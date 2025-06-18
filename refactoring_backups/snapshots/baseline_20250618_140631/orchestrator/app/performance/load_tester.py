"""
K6 Load Testing Infrastructure
Comprehensive load testing setup for performance validation and benchmarking.
"""

import asyncio
import json
import logging
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from ..config import config
from ..observability.monitoring import monitoring_manager


logger = logging.getLogger(__name__)


@dataclass
class LoadTestConfig:
    """Load test configuration"""
    name: str
    duration: str = "5m"
    virtual_users: int = 100
    ramp_up_duration: str = "30s"
    ramp_down_duration: str = "30s"
    target_rps: Optional[int] = None
    max_response_time: int = 2000  # ms
    error_rate_threshold: float = 5.0  # %
    endpoints: List[str] = None
    custom_headers: Dict[str, str] = None
    data_payloads: Dict[str, Any] = None


@dataclass
class LoadTestResult:
    """Load test execution result"""
    test_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    error_rate: float
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    max_response_time: float
    requests_per_second: float
    data_received_mb: float
    data_sent_mb: float
    virtual_users: int
    status: str  # passed, failed, error
    errors: List[str] = None


class K6LoadTester:
    """K6 Load Testing Manager"""
    
    def __init__(self):
        self.base_url = getattr(config, "LOAD_TEST_BASE_URL", "http://localhost:8000")
        self.results_dir = Path(getattr(config, "LOAD_TEST_RESULTS_DIR", "/tmp/k6_results"))
        self.scripts_dir = Path(getattr(config, "LOAD_TEST_SCRIPTS_DIR", "/tmp/k6_scripts"))
        
        # Ensure directories exist
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Default test configurations
        self.test_configs = self._initialize_test_configs()
        
        # Performance benchmarks
        self.performance_targets = {
            "max_response_time_p95": 200,  # ms
            "max_response_time_p99": 500,  # ms
            "min_requests_per_second": 1000,
            "max_error_rate": 1.0,  # %
            "max_cpu_usage": 80.0,  # %
            "max_memory_usage": 85.0  # %
        }
    
    def _initialize_test_configs(self) -> Dict[str, LoadTestConfig]:
        """Initialize default test configurations"""
        return {
            "smoke": LoadTestConfig(
                name="Smoke Test",
                duration="2m",
                virtual_users=5,
                ramp_up_duration="10s",
                ramp_down_duration="10s",
                endpoints=["/health", "/metrics"]
            ),
            "load": LoadTestConfig(
                name="Load Test",
                duration="10m",
                virtual_users=100,
                ramp_up_duration="2m",
                ramp_down_duration="1m",
                target_rps=500,
                endpoints=["/health", "/api/v1/orchestrate", "/api/v1/status"]
            ),
            "stress": LoadTestConfig(
                name="Stress Test",
                duration="15m",
                virtual_users=500,
                ramp_up_duration="5m",
                ramp_down_duration="2m",
                target_rps=1000,
                endpoints=["/api/v1/orchestrate", "/api/v1/agents", "/api/v1/memory"]
            ),
            "spike": LoadTestConfig(
                name="Spike Test",
                duration="10m",
                virtual_users=1000,
                ramp_up_duration="30s",
                ramp_down_duration="30s",
                target_rps=2000,
                endpoints=["/api/v1/orchestrate"]
            ),
            "soak": LoadTestConfig(
                name="Soak Test",
                duration="60m",
                virtual_users=50,
                ramp_up_duration="2m",
                ramp_down_duration="2m",
                target_rps=200,
                endpoints=["/api/v1/orchestrate", "/api/v1/status", "/health"]
            ),
            "security": LoadTestConfig(
                name="Security Test",
                duration="5m",
                virtual_users=50,
                endpoints=["/admin", "/secrets", "/config"],
                custom_headers={"Authorization": "Bearer invalid_token"}
            )
        }
    
    def _generate_k6_script(self, config: LoadTestConfig) -> str:
        """Generate K6 JavaScript test script"""
        endpoints = config.endpoints or ["/health"]
        
        script = f"""
import http from 'k6/http';
import {{ check, sleep }} from 'k6';
import {{ Rate }} from 'k6/metrics';

// Custom metrics
export let errorRate = new Rate('errors');

// Test configuration
export let options = {{
    stages: [
        {{ duration: '{config.ramp_up_duration}', target: {config.virtual_users} }},
        {{ duration: '{config.duration}', target: {config.virtual_users} }},
        {{ duration: '{config.ramp_down_duration}', target: 0 }},
    ],
    thresholds: {{
        http_req_duration: ['p(95)<{config.max_response_time}'],
        http_req_failed: ['rate<{config.error_rate_threshold/100}'],
        errors: ['rate<{config.error_rate_threshold/100}'],
    }},
    ext: {{
        loadimpact: {{
            name: '{config.name}',
            distribution: {{
                'amazon:us:ashburn': {{ loadZone: 'amazon:us:ashburn', percent: 100 }},
            }},
        }},
    }},
}};

// Base URL
const BASE_URL = '{self.base_url}';

// Test endpoints
const ENDPOINTS = {json.dumps(endpoints)};

// Headers
const HEADERS = {json.dumps(config.custom_headers or {})};

// Test data payloads
const PAYLOADS = {json.dumps(config.data_payloads or {})};

export default function () {{
    // Select random endpoint
    const endpoint = ENDPOINTS[Math.floor(Math.random() * ENDPOINTS.length)];
    const url = `${{BASE_URL}}${{endpoint}}`;
    
    // Prepare request parameters
    let params = {{
        headers: {{
            'Content-Type': 'application/json',
            'User-Agent': 'K6-LoadTest/{config.name}',
            ...HEADERS
        }},
        timeout: '30s',
    }};
    
    let response;
    
    // Handle different request types based on endpoint
    if (endpoint.includes('/orchestrate') && PAYLOADS.orchestrate) {{
        // POST request for orchestration
        response = http.post(url, JSON.stringify(PAYLOADS.orchestrate), params);
    }} else if (endpoint.includes('/memory') && PAYLOADS.memory) {{
        // POST request for memory operations
        response = http.post(url, JSON.stringify(PAYLOADS.memory), params);
    }} else {{
        // GET request for other endpoints
        response = http.get(url, params);
    }}
    
    // Check response
    let checkResult = check(response, {{
        'status is 200-299': (r) => r.status >= 200 && r.status < 300,
        'response time < {config.max_response_time}ms': (r) => r.timings.duration < {config.max_response_time},
        'response has body': (r) => r.body && r.body.length > 0,
    }});
    
    // Record errors
    errorRate.add(!checkResult);
    
    // Simulate user think time
    sleep(Math.random() * 2 + 1); // 1-3 seconds
}}

export function handleSummary(data) {{
    return {{
        '{self.results_dir / f"{config.name.lower().replace(' ', '_')}_results.json"}': JSON.stringify(data, null, 2),
        stdout: textSummary(data, {{ indent: ' ', enableColors: true }}),
    }};
}}

function textSummary(data, options) {{
    const indent = options.indent || '';
    const enableColors = options.enableColors || false;
    
    let summary = `
${{indent}}✓ {config.name} Results:
${{indent}}  Total Requests: ${{data.metrics.http_reqs.count}}
${{indent}}  Failed Requests: ${{data.metrics.http_req_failed.count}}
${{indent}}  Error Rate: ${{(data.metrics.http_req_failed.rate * 100).toFixed(2)}}%
${{indent}}  Avg Response Time: ${{data.metrics.http_req_duration.avg.toFixed(2)}}ms
${{indent}}  P95 Response Time: ${{data.metrics['http_req_duration{{p(95)}}'].value.toFixed(2)}}ms
${{indent}}  P99 Response Time: ${{data.metrics['http_req_duration{{p(99)}}'].value.toFixed(2)}}ms
${{indent}}  Requests/sec: ${{data.metrics.http_reqs.rate.toFixed(2)}}
${{indent}}  Data Received: ${{(data.metrics.data_received.count / 1024 / 1024).toFixed(2)}} MB
${{indent}}  Data Sent: ${{(data.metrics.data_sent.count / 1024 / 1024).toFixed(2)}} MB
`;
    
    return summary;
}}
"""
        
        return script
    
    async def run_test(self, test_name: str, custom_config: Optional[LoadTestConfig] = None) -> LoadTestResult:
        """Run a specific load test"""
        config = custom_config or self.test_configs.get(test_name)
        if not config:
            raise ValueError(f"Unknown test configuration: {test_name}")
        
        logger.info(f"Starting load test: {config.name}")
        
        # Generate K6 script
        script_content = self._generate_k6_script(config)
        script_path = self.scripts_dir / f"{test_name}.js"
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Prepare results file
        results_file = self.results_dir / f"{test_name}_results.json"
        
        start_time = datetime.utcnow()
        
        try:
            # Run K6 test
            cmd = [
                "k6", "run",
                "--out", f"json={results_file}",
                str(script_path)
            ]
            
            # Add environment variables
            env = {
                "K6_NO_USAGE_REPORT": "true",
                "K6_NO_CLOUD": "true"
            }
            
            logger.info(f"Executing K6 command: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await process.communicate()
            
            end_time = datetime.utcnow()
            
            # Parse results
            if process.returncode == 0 and results_file.exists():
                result = await self._parse_k6_results(results_file, config, start_time, end_time)
                result.status = "passed" if self._validate_performance(result) else "failed"
            else:
                result = LoadTestResult(
                    test_name=config.name,
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=(end_time - start_time).total_seconds(),
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=0,
                    error_rate=100.0,
                    avg_response_time=0,
                    p95_response_time=0,
                    p99_response_time=0,
                    max_response_time=0,
                    requests_per_second=0,
                    data_received_mb=0,
                    data_sent_mb=0,
                    virtual_users=config.virtual_users,
                    status="error",
                    errors=[stderr.decode() if stderr else "Unknown error"]
                )
            
            # Log results
            logger.info(f"Load test completed: {result.status}")
            logger.info(f"Requests: {result.total_requests}, RPS: {result.requests_per_second:.2f}, P95: {result.p95_response_time:.2f}ms")
            
            # Update monitoring
            await self._update_load_test_metrics(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error running load test {test_name}: {e}")
            end_time = datetime.utcnow()
            
            return LoadTestResult(
                test_name=config.name,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=(end_time - start_time).total_seconds(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                error_rate=100.0,
                avg_response_time=0,
                p95_response_time=0,
                p99_response_time=0,
                max_response_time=0,
                requests_per_second=0,
                data_received_mb=0,
                data_sent_mb=0,
                virtual_users=config.virtual_users,
                status="error",
                errors=[str(e)]
            )
    
    async def _parse_k6_results(self, results_file: Path, config: LoadTestConfig, 
                               start_time: datetime, end_time: datetime) -> LoadTestResult:
        """Parse K6 results from JSON output"""
        try:
            with open(results_file, 'r') as f:
                # K6 outputs NDJSON (newline-delimited JSON)
                lines = f.readlines()
                
                # Find the summary line (last line with 'type': 'summary')
                summary_data = None
                for line in reversed(lines):
                    try:
                        data = json.loads(line.strip())
                        if data.get('type') == 'summary':
                            summary_data = data['data']
                            break
                    except json.JSONDecodeError:
                        continue
                
                if not summary_data:
                    raise ValueError("No summary data found in K6 results")
                
                metrics = summary_data['metrics']
                
                # Extract key metrics
                http_reqs = metrics.get('http_reqs', {})
                http_req_duration = metrics.get('http_req_duration', {})
                http_req_failed = metrics.get('http_req_failed', {})
                data_received = metrics.get('data_received', {})
                data_sent = metrics.get('data_sent', {})
                
                total_requests = http_reqs.get('count', 0)
                failed_requests = http_req_failed.get('count', 0)
                successful_requests = total_requests - failed_requests
                
                result = LoadTestResult(
                    test_name=config.name,
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=(end_time - start_time).total_seconds(),
                    total_requests=total_requests,
                    successful_requests=successful_requests,
                    failed_requests=failed_requests,
                    error_rate=http_req_failed.get('rate', 0) * 100,
                    avg_response_time=http_req_duration.get('avg', 0),
                    p95_response_time=metrics.get('http_req_duration{p(95)}', {}).get('value', 0),
                    p99_response_time=metrics.get('http_req_duration{p(99)}', {}).get('value', 0),
                    max_response_time=http_req_duration.get('max', 0),
                    requests_per_second=http_reqs.get('rate', 0),
                    data_received_mb=data_received.get('count', 0) / 1024 / 1024,
                    data_sent_mb=data_sent.get('count', 0) / 1024 / 1024,
                    virtual_users=config.virtual_users
                )
                
                return result
                
        except Exception as e:
            logger.error(f"Error parsing K6 results: {e}")
            raise
    
    def _validate_performance(self, result: LoadTestResult) -> bool:
        """Validate if performance meets targets"""
        validations = []
        
        # Check response times
        if result.p95_response_time > self.performance_targets["max_response_time_p95"]:
            validations.append(f"P95 response time too high: {result.p95_response_time}ms > {self.performance_targets['max_response_time_p95']}ms")
        
        if result.p99_response_time > self.performance_targets["max_response_time_p99"]:
            validations.append(f"P99 response time too high: {result.p99_response_time}ms > {self.performance_targets['max_response_time_p99']}ms")
        
        # Check requests per second
        if result.requests_per_second < self.performance_targets["min_requests_per_second"]:
            validations.append(f"RPS too low: {result.requests_per_second} < {self.performance_targets['min_requests_per_second']}")
        
        # Check error rate
        if result.error_rate > self.performance_targets["max_error_rate"]:
            validations.append(f"Error rate too high: {result.error_rate}% > {self.performance_targets['max_error_rate']}%")
        
        if validations:
            logger.warning(f"Performance validation failed: {'; '.join(validations)}")
            return False
        
        return True
    
    async def _update_load_test_metrics(self, result: LoadTestResult):
        """Update monitoring with load test metrics"""
        try:
            labels = {"test_name": result.test_name}
            
            await monitoring_manager.record_metric("load_test_requests_total", result.total_requests, labels)
            await monitoring_manager.record_metric("load_test_error_rate", result.error_rate, labels)
            await monitoring_manager.record_metric("load_test_response_time_p95", result.p95_response_time, labels)
            await monitoring_manager.record_metric("load_test_requests_per_second", result.requests_per_second, labels)
            await monitoring_manager.record_metric("load_test_duration", result.duration_seconds, labels)
            
        except Exception as e:
            logger.error(f"Error updating load test metrics: {e}")
    
    async def run_performance_suite(self) -> Dict[str, LoadTestResult]:
        """Run complete performance test suite"""
        logger.info("Starting complete performance test suite")
        
        suite_results = {}
        test_order = ["smoke", "load", "stress", "spike", "soak"]
        
        for test_name in test_order:
            try:
                logger.info(f"Running {test_name} test...")
                result = await self.run_test(test_name)
                suite_results[test_name] = result
                
                # If smoke test fails, stop the suite
                if test_name == "smoke" and result.status != "passed":
                    logger.error("Smoke test failed, stopping test suite")
                    break
                
                # Brief pause between tests
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in {test_name} test: {e}")
                suite_results[test_name] = LoadTestResult(
                    test_name=test_name,
                    start_time=datetime.utcnow(),
                    end_time=datetime.utcnow(),
                    duration_seconds=0,
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=0,
                    error_rate=100.0,
                    avg_response_time=0,
                    p95_response_time=0,
                    p99_response_time=0,
                    max_response_time=0,
                    requests_per_second=0,
                    data_received_mb=0,
                    data_sent_mb=0,
                    virtual_users=0,
                    status="error",
                    errors=[str(e)]
                )
        
        # Generate comprehensive report
        await self._generate_performance_report(suite_results)
        
        return suite_results
    
    async def _generate_performance_report(self, results: Dict[str, LoadTestResult]):
        """Generate comprehensive performance report"""
        report_path = self.results_dir / f"performance_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
        
        # Calculate overall statistics
        total_requests = sum(r.total_requests for r in results.values())
        total_errors = sum(r.failed_requests for r in results.values())
        avg_error_rate = sum(r.error_rate for r in results.values()) / len(results) if results else 0
        max_rps = max(r.requests_per_second for r in results.values()) if results else 0
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 5px; flex: 1; }}
        .metric.passed {{ border-left: 5px solid #28a745; }}
        .metric.failed {{ border-left: 5px solid #dc3545; }}
        .metric.error {{ border-left: 5px solid #fd7e14; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .status-passed {{ color: #28a745; font-weight: bold; }}
        .status-failed {{ color: #dc3545; font-weight: bold; }}
        .status-error {{ color: #fd7e14; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Performance Test Report</h1>
        <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        <p><strong>Base URL:</strong> {self.base_url}</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Requests</h3>
            <h2>{total_requests:,}</h2>
        </div>
        <div class="metric">
            <h3>Total Errors</h3>
            <h2>{total_errors:,}</h2>
        </div>
        <div class="metric">
            <h3>Avg Error Rate</h3>
            <h2>{avg_error_rate:.2f}%</h2>
        </div>
        <div class="metric">
            <h3>Peak RPS</h3>
            <h2>{max_rps:.0f}</h2>
        </div>
    </div>
    
    <h2>📊 Test Results</h2>
    <table>
        <thead>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Total Requests</th>
                <th>Error Rate</th>
                <th>Avg Response Time</th>
                <th>P95 Response Time</th>
                <th>P99 Response Time</th>
                <th>Requests/sec</th>
                <th>Duration</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for test_name, result in results.items():
            status_class = f"status-{result.status}"
            html_content += f"""
            <tr>
                <td>{result.test_name}</td>
                <td class="{status_class}">{result.status.upper()}</td>
                <td>{result.total_requests:,}</td>
                <td>{result.error_rate:.2f}%</td>
                <td>{result.avg_response_time:.2f}ms</td>
                <td>{result.p95_response_time:.2f}ms</td>
                <td>{result.p99_response_time:.2f}ms</td>
                <td>{result.requests_per_second:.2f}</td>
                <td>{result.duration_seconds:.0f}s</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
    
    <h2>🎯 Performance Targets</h2>
    <ul>
"""
        
        for target, value in self.performance_targets.items():
            html_content += f"<li><strong>{target}:</strong> {value}</li>"
        
        html_content += """
    </ul>
    
    <h2>📈 Recommendations</h2>
    <ul>
        <li>Monitor response times during peak load</li>
        <li>Implement cache warming strategies for better performance</li>
        <li>Consider horizontal scaling if RPS targets are not met</li>
        <li>Optimize database queries for sub-200ms response times</li>
        <li>Implement circuit breakers for improved error handling</li>
    </ul>
</body>
</html>
"""
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Performance report generated: {report_path}")
    
    async def get_test_configs(self) -> Dict[str, Dict]:
        """Get all available test configurations"""
        return {name: asdict(config) for name, config in self.test_configs.items()}
    
    async def update_performance_targets(self, targets: Dict[str, Any]):
        """Update performance targets"""
        self.performance_targets.update(targets)
        logger.info(f"Performance targets updated: {targets}")


# Global instance
load_tester = K6LoadTester()
