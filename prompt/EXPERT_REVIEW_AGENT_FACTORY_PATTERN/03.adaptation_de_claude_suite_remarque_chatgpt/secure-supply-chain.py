# === OPA Policy pour Templates ===

# policy/agent_templates.rego
"""
package agent_factory.templates

import future.keywords.if
import future.keywords.contains

# Règle principale : un template est autorisé si toutes les checks passent
allow if {
    valid_structure
    no_dangerous_patterns
    resource_limits_ok
    approved_capabilities
    signed_template
}

# Structure valide
valid_structure if {
    input.template.name
    input.template.role
    input.template.domain
    input.template.capabilities
}

# Pas de patterns dangereux
no_dangerous_patterns if {
    not contains_dangerous_code
}

contains_dangerous_code if {
    patterns := [
        "eval", "exec", "__import__", "subprocess",
        "os.system", "open(", "file("
    ]
    some pattern in patterns
    contains(input.template_string, pattern)
}

# Limites de ressources respectées
resource_limits_ok if {
    input.template.resource_limits.memory_mb <= 4096
    input.template.resource_limits.cpu_percent <= 80
    input.template.resource_limits.timeout_seconds <= 300
}

# Capacités approuvées uniquement
approved_capabilities if {
    allowed := {
        "analysis", "generation", "transformation",
        "validation", "monitoring", "orchestration"
    }
    all_approved := {cap | 
        cap := input.template.capabilities[_]
        cap in allowed
    }
    count(all_approved) == count(input.template.capabilities)
}

# Template signé
signed_template if {
    input.signature
    input.signature != ""
}

# Règles spécifiques par domaine
domain_specific_rules["security"] := {
    "max_memory_mb": 8192,
    "required_capabilities": ["analysis", "monitoring"],
    "forbidden_tools": ["root_access", "kernel_module"]
}

domain_specific_rules["public"] := {
    "max_memory_mb": 1024,
    "required_capabilities": ["analysis"],
    "forbidden_tools": ["network_scan", "file_system"]
}
"""

# === Intégration Cosign et SBOM ===

import subprocess
import json
import hashlib
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import aiofiles
import asyncio
from datetime import datetime

@dataclass
class SignatureInfo:
    """Information de signature Cosign"""
    signature: str
    certificate: Optional[str]
    timestamp: datetime
    signed_by: str
    payload_hash: str

class CosignIntegration:
    """Intégration Cosign pour signature de templates et images"""
    
    def __init__(
        self,
        private_key_path: str,
        public_key_path: str,
        rekor_url: str = "https://rekor.sigstore.dev"
    ):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        self.rekor_url = rekor_url
    
    async def sign_template(
        self,
        template: Dict[str, Any],
        signer_email: str
    ) -> SignatureInfo:
        """Signe un template avec Cosign"""
        
        # Sérialiser le template
        template_json = json.dumps(template, sort_keys=True)
        template_hash = hashlib.sha256(template_json.encode()).hexdigest()
        
        # Créer un fichier temporaire
        temp_file = f"/tmp/template_{template_hash}.json"
        async with aiofiles.open(temp_file, 'w') as f:
            await f.write(template_json)
        
        try:
            # Signer avec Cosign
            cmd = [
                "cosign", "sign-blob",
                "--key", self.private_key_path,
                "--output-signature", f"{temp_file}.sig",
                "--output-certificate", f"{temp_file}.crt",
                "--tlog-upload=true",
                temp_file
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Cosign signing failed: {stderr.decode()}")
            
            # Lire la signature
            async with aiofiles.open(f"{temp_file}.sig", 'rb') as f:
                signature = await f.read()
            
            # Lire le certificat si disponible
            certificate = None
            try:
                async with aiofiles.open(f"{temp_file}.crt", 'r') as f:
                    certificate = await f.read()
            except:
                pass
            
            return SignatureInfo(
                signature=base64.b64encode(signature).decode(),
                certificate=certificate,
                timestamp=datetime.utcnow(),
                signed_by=signer_email,
                payload_hash=template_hash
            )
            
        finally:
            # Nettoyage
            for ext in ['', '.sig', '.crt']:
                try:
                    os.unlink(f"{temp_file}{ext}")
                except:
                    pass
    
    async def verify_template(
        self,
        template: Dict[str, Any],
        signature: str,
        certificate: Optional[str] = None
    ) -> bool:
        """Vérifie la signature d'un template"""
        
        # Recréer le hash
        template_json = json.dumps(template, sort_keys=True)
        template_hash = hashlib.sha256(template_json.encode()).hexdigest()
        
        # Fichiers temporaires
        temp_file = f"/tmp/verify_{template_hash}.json"
        sig_file = f"/tmp/verify_{template_hash}.sig"
        
        try:
            # Écrire le template et la signature
            async with aiofiles.open(temp_file, 'w') as f:
                await f.write(template_json)
            
            async with aiofiles.open(sig_file, 'wb') as f:
                await f.write(base64.b64decode(signature))
            
            # Vérifier avec Cosign
            cmd = [
                "cosign", "verify-blob",
                "--key", self.public_key_path,
                "--signature", sig_file,
                temp_file
            ]
            
            if certificate:
                cert_file = f"/tmp/verify_{template_hash}.crt"
                async with aiofiles.open(cert_file, 'w') as f:
                    await f.write(certificate)
                cmd.extend(["--certificate", cert_file])
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            return process.returncode == 0
            
        finally:
            # Nettoyage
            for file in [temp_file, sig_file]:
                try:
                    os.unlink(file)
                except:
                    pass

# === SBOM Generation ===

@dataclass
class SBOMComponent:
    """Composant SBOM"""
    name: str
    version: str
    type: str  # library, framework, tool
    license: Optional[str]
    vulnerabilities: List[str] = None

class SBOMGenerator:
    """Générateur de Software Bill of Materials"""
    
    def __init__(self):
        self.vulnerability_db = {}  # Cache des CVE
    
    async def generate_sbom(
        self,
        template: Dict[str, Any],
        scan_vulnerabilities: bool = True
    ) -> Dict[str, Any]:
        """Génère un SBOM pour un template"""
        
        components = []
        
        # Analyser les dépendances Python
        if "requirements" in template:
            for req in template["requirements"]:
                component = await self._analyze_python_package(req)
                components.append(component)
        
        # Analyser les outils
        if "tools" in template:
            for tool in template["tools"]:
                component = await self._analyze_tool(tool)
                components.append(component)
        
        # Scanner les vulnérabilités si demandé
        if scan_vulnerabilities:
            for component in components:
                component.vulnerabilities = await self._scan_vulnerabilities(
                    component.name, component.version
                )
        
        # Générer le SBOM au format SPDX
        sbom = {
            "spdxVersion": "SPDX-2.3",
            "creationInfo": {
                "created": datetime.utcnow().isoformat(),
                "creators": ["Tool: agent-factory-sbom-generator"]
            },
            "name": f"SBOM for {template['name']}",
            "packages": [
                {
                    "name": comp.name,
                    "version": comp.version,
                    "downloadLocation": f"https://pypi.org/project/{comp.name}/",
                    "licenseConcluded": comp.license or "NOASSERTION",
                    "vulnerabilities": comp.vulnerabilities or []
                }
                for comp in components
            ]
        }
        
        return sbom
    
    async def _analyze_python_package(self, requirement: str) -> SBOMComponent:
        """Analyse un package Python"""
        # Parser le requirement (simplifié)
        if "==" in requirement:
            name, version = requirement.split("==")
        elif ">=" in requirement:
            name = requirement.split(">=")[0]
            version = "latest"
        else:
            name = requirement
            version = "unspecified"
        
        # En production : utiliser pip-api ou similar
        return SBOMComponent(
            name=name.strip(),
            version=version.strip(),
            type="library",
            license=await self._get_package_license(name)
        )
    
    async def _scan_vulnerabilities(
        self,
        package: str,
        version: str
    ) -> List[str]:
        """Scanne les vulnérabilités connues"""
        
        # En production : utiliser OSV API ou Grype
        cmd = [
            "grype", 
            f"{package}:{version}",
            "--output", "json"
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                results = json.loads(stdout.decode())
                return [
                    vuln["vulnerability"]["id"] 
                    for vuln in results.get("matches", [])
                ]
        except:
            pass
        
        return []

# === Validation complète avec OPA ===

class SecureTemplateValidator:
    """Validateur sécurisé avec OPA, Cosign et SBOM"""
    
    def __init__(
        self,
        opa_url: str,
        cosign_integration: CosignIntegration,
        sbom_generator: SBOMGenerator
    ):
        self.opa_url = opa_url
        self.cosign = cosign_integration
        self.sbom_gen = sbom_generator
    
    async def validate_template(
        self,
        template: Dict[str, Any],
        signature: Optional[str] = None,
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Validation complète d'un template"""
        
        validation_results = {
            "valid": True,
            "checks": {},
            "sbom": None,
            "recommendations": []
        }
        
        # 1. Validation OPA
        opa_result = await self._validate_with_opa(template, user_context)
        validation_results["checks"]["opa_policy"] = opa_result["allow"]
        
        if not opa_result["allow"]:
            validation_results["valid"] = False
            validation_results["recommendations"].append(
                f"OPA policy violation: {opa_result.get('reason', 'Unknown')}"
            )
        
        # 2. Vérification de signature
        if signature:
            sig_valid = await self.cosign.verify_template(template, signature)
            validation_results["checks"]["signature"] = sig_valid
            
            if not sig_valid:
                validation_results["valid"] = False
                validation_results["recommendations"].append(
                    "Invalid or missing signature. Template must be signed with approved key."
                )
        else:
            validation_results["checks"]["signature"] = False
            validation_results["recommendations"].append(
                "Template should be signed for production use."
            )
        
        # 3. Génération et analyse SBOM
        sbom = await self.sbom_gen.generate_sbom(template, scan_vulnerabilities=True)
        validation_results["sbom"] = sbom
        
        # Analyser les vulnérabilités
        critical_vulns = []
        for package in sbom["packages"]:
            for vuln in package.get("vulnerabilities", []):
                if vuln.startswith("CRITICAL") or vuln.startswith("HIGH"):
                    critical_vulns.append(f"{package['name']}: {vuln}")
        
        if critical_vulns:
            validation_results["checks"]["vulnerabilities"] = False
            validation_results["valid"] = False
            validation_results["recommendations"].extend([
                f"Critical vulnerability found: {vuln}" for vuln in critical_vulns
            ])
        else:
            validation_results["checks"]["vulnerabilities"] = True
        
        # 4. Validation des ressources
        resource_check = self._validate_resources(template)
        validation_results["checks"]["resources"] = resource_check["valid"]
        
        if not resource_check["valid"]:
            validation_results["valid"] = False
            validation_results["recommendations"].extend(resource_check["issues"])
        
        return validation_results
    
    async def _validate_with_opa(
        self,
        template: Dict[str, Any],
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Appel à OPA pour validation"""
        
        # Préparer l'input pour OPA
        opa_input = {
            "template": template,
            "template_string": json.dumps(template),
            "user": user_context or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Appel HTTP à OPA
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.opa_url}/v1/data/agent_factory/templates/allow",
                json={"input": opa_input}
            ) as response:
                result = await response.json()
        
        return result.get("result", {"allow": False, "reason": "OPA unavailable"})
    
    def _validate_resources(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Valide les limites de ressources"""
        
        issues = []
        limits = template.get("resource_limits", {})
        
        # Vérifications par domaine
        domain = template.get("domain", "general")
        domain_limits = {
            "public": {"memory_mb": 1024, "cpu_percent": 25},
            "internal": {"memory_mb": 4096, "cpu_percent": 50},
            "critical": {"memory_mb": 8192, "cpu_percent": 80}
        }
        
        max_limits = domain_limits.get(domain, domain_limits["internal"])
        
        if limits.get("memory_mb", 0) > max_limits["memory_mb"]:
            issues.append(
                f"Memory limit {limits['memory_mb']}MB exceeds maximum "
                f"{max_limits['memory_mb']}MB for domain '{domain}'"
            )
        
        if limits.get("cpu_percent", 0) > max_limits["cpu_percent"]:
            issues.append(
                f"CPU limit {limits['cpu_percent']}% exceeds maximum "
                f"{max_limits['cpu_percent']}% for domain '{domain}'"
            )
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

# === Kubernetes Admission Controller ===

from kubernetes import client, config
from kubernetes.client.rest import ApiException
import base64

class AgentAdmissionController:
    """Admission controller pour valider les déploiements d'agents"""
    
    def __init__(self, validator: SecureTemplateValidator):
        self.validator = validator
        config.load_incluster_config()  # En production
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    async def validate_admission(
        self,
        admission_review: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Webhook d'admission pour Kubernetes"""
        
        request = admission_review["request"]
        
        # Extraire les informations du pod/deployment
        object_kind = request["kind"]["kind"]
        object_name = request["name"]
        
        # Vérifier les annotations
        annotations = request["object"]["metadata"].get("annotations", {})
        
        # Template associé
        template_name = annotations.get("agent-factory.io/template")
        template_signature = annotations.get("agent-factory.io/signature")
        
        if not template_name:
            return self._deny_response("Missing template annotation")
        
        # Charger et valider le template
        template = await self._load_template(template_name)
        
        validation_result = await self.validator.validate_template(
            template,
            signature=template_signature,
            user_context={"namespace": request["namespace"]}
        )
        
        if not validation_result["valid"]:
            reasons = "\n".join(validation_result["recommendations"])
            return self._deny_response(f"Template validation failed:\n{reasons}")
        
        # Vérifier l'image du conteneur
        containers = request["object"]["spec"].get("containers", [])
        for container in containers:
            image = container["image"]
            if not await self._verify_image_signature(image):
                return self._deny_response(f"Image {image} is not signed")
        
        # Appliquer les mutations si nécessaire
        patches = self._generate_security_patches(template, request["object"])
        
        return self._allow_response(patches)
    
    async def _verify_image_signature(self, image: str) -> bool:
        """Vérifie la signature d'une image avec Cosign"""
        
        cmd = [
            "cosign", "verify",
            "--key", "/keys/cosign.pub",
            image
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()
        return process.returncode == 0
    
    def _generate_security_patches(
        self,
        template: Dict[str, Any],
        pod_spec: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des patches pour sécuriser le pod"""
        
        patches = []
        
        # Ajouter les SecurityContext
        patches.append({
            "op": "add",
            "path": "/spec/securityContext",
            "value": {
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "fsGroup": 1000,
                "seccompProfile": {
                    "type": "RuntimeDefault"
                }
            }
        })
        
        # Limites de ressources depuis le template
        limits = template.get("resource_limits", {})
        for i, container in enumerate(pod_spec["spec"].get("containers", [])):
            patches.append({
                "op": "add",
                "path": f"/spec/containers/{i}/resources",
                "value": {
                    "limits": {
                        "memory": f"{limits.get('memory_mb', 1024)}Mi",
                        "cpu": f"{limits.get('cpu_percent', 50) / 100}"
                    },
                    "requests": {
                        "memory": f"{limits.get('memory_mb', 1024) // 2}Mi",
                        "cpu": f"{limits.get('cpu_percent', 50) / 200}"
                    }
                }
            })
            
            # Security context du conteneur
            patches.append({
                "op": "add",
                "path": f"/spec/containers/{i}/securityContext",
                "value": {
                    "allowPrivilegeEscalation": False,
                    "readOnlyRootFilesystem": True,
                    "capabilities": {
                        "drop": ["ALL"]
                    }
                }
            })
        
        return patches
    
    def _allow_response(self, patches: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Réponse d'autorisation avec patches optionnels"""
        response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": True,
                "uid": "",  # Sera rempli par K8s
            }
        }
        
        if patches:
            response["response"]["patchType"] = "JSONPatch"
            response["response"]["patch"] = base64.b64encode(
                json.dumps(patches).encode()
            ).decode()
        
        return response
    
    def _deny_response(self, reason: str) -> Dict[str, Any]:
        """Réponse de refus avec raison"""
        return {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": False,
                "uid": "",  # Sera rempli par K8s
                "status": {
                    "message": reason
                }
            }
        }

# === CI/CD Pipeline Security ===

class SecureCIPipeline:
    """Pipeline CI/CD sécurisé pour les agents"""
    
    def __init__(
        self,
        cosign: CosignIntegration,
        validator: SecureTemplateValidator
    ):
        self.cosign = cosign
        self.validator = validator
    
    async def validate_and_sign_template(
        self,
        template_path: str,
        signer_email: str
    ) -> Dict[str, Any]:
        """Valide et signe un template dans le pipeline CI"""
        
        # Charger le template
        async with aiofiles.open(template_path, 'r') as f:
            template_content = await f.read()
        
        template = json.loads(template_content)
        
        # 1. Validation complète
        validation = await self.validator.validate_template(template)
        
        if not validation["valid"]:
            raise Exception(
                f"Template validation failed: {validation['recommendations']}"
            )
        
        # 2. Signature
        signature_info = await self.cosign.sign_template(template, signer_email)
        
        # 3. Créer le bundle signé
        signed_bundle = {
            "template": template,
            "signature": signature_info.signature,
            "certificate": signature_info.certificate,
            "sbom": validation["sbom"],
            "validation_report": validation,
            "metadata": {
                "signed_at": signature_info.timestamp.isoformat(),
                "signed_by": signer_email,
                "template_hash": signature_info.payload_hash
            }
        }
        
        # 4. Sauvegarder le bundle
        bundle_path = template_path.replace(".json", ".signed.json")
        async with aiofiles.open(bundle_path, 'w') as f:
            await f.write(json.dumps(signed_bundle, indent=2))
        
        # 5. Upload vers registry sécurisé (S3, etc.)
        await self._upload_to_registry(signed_bundle)
        
        return signed_bundle
    
    async def _upload_to_registry(self, bundle: Dict[str, Any]):
        """Upload le bundle vers un registry sécurisé"""
        # Implémentation S3 ou similaire
        pass

# === Exemple d'utilisation complète ===

async def secure_template_example():
    """Exemple de supply chain sécurisée"""
    
    # Configuration
    cosign = CosignIntegration(
        private_key_path="/keys/cosign.key",
        public_key_path="/keys/cosign.pub"
    )
    
    sbom_gen = SBOMGenerator()
    
    validator = SecureTemplateValidator(
        opa_url="http://opa:8181",
        cosign_integration=cosign,
        sbom_generator=sbom_gen
    )
    
    # Template exemple
    template = {
        "name": "secure_processor",
        "role": "data_processor",
        "domain": "internal",
        "capabilities": ["analysis", "transformation"],
        "requirements": [
            "langchain==0.1.0",
            "numpy==1.24.0",
            "pandas==2.0.0"
        ],
        "tools": ["python", "git"],
        "resource_limits": {
            "memory_mb": 2048,
            "cpu_percent": 50,
            "timeout_seconds": 180
        }
    }
    
    # 1. Validation et signature dans CI/CD
    pipeline = SecureCIPipeline(cosign, validator)
    
    # Sauver le template
    async with aiofiles.open("/tmp/template.json", 'w') as f:
        await f.write(json.dumps(template))
    
    # Valider et signer
    signed_bundle = await pipeline.validate_and_sign_template(
        "/tmp/template.json",
        "ci@example.com"
    )
    
    print(f"Template signed: {signed_bundle['metadata']['template_hash']}")
    print(f"SBOM generated with {len(signed_bundle['sbom']['packages'])} components")
    
    # 2. Admission controller en action
    admission_controller = AgentAdmissionController(validator)
    
    # Simuler une requête d'admission
    admission_request = {
        "request": {
            "uid": "test-123",
            "kind": {"kind": "Pod"},
            "name": "agent-test",
            "namespace": "agents",
            "object": {
                "metadata": {
                    "name": "agent-test",
                    "annotations": {
                        "agent-factory.io/template": "secure_processor",
                        "agent-factory.io/signature": signed_bundle["signature"]
                    }
                },
                "spec": {
                    "containers": [{
                        "name": "agent",
                        "image": "agent-factory/processor:v1.0"
                    }]
                }
            }
        }
    }
    
    response = await admission_controller.validate_admission(admission_request)
    print(f"Admission decision: {response['response']['allowed']}")
    
    # 3. Rapport de validation
    print("\n=== Validation Report ===")
    for check, result in signed_bundle["validation_report"]["checks"].items():
        print(f"{check}: {'✓' if result else '✗'}")
    
    if signed_bundle["validation_report"]["recommendations"]:
        print("\nRecommendations:")
        for rec in signed_bundle["validation_report"]["recommendations"]:
            print(f"- {rec}")

if __name__ == "__main__":
    asyncio.run(secure_template_example())