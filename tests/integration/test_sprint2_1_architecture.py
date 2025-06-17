"""
Integration tests for Sprint 2.1 Architecture components
Tests memory optimization, state management, and agent coordination.
"""

import asyncio
import pytest
import json
from datetime import datetime, timedelta
from typing import Dict, Any

from orchestrator.app.performance.memory_optimizer import AdvancedMemoryManager
from orchestrator.app.agents.advanced_state_manager import AdvancedStateManager, StateCompressionType
from orchestrator.app.agents.advanced_coordination import (
    AdvancedAgentCoordinator, AgentTask, AgentPriority, ResourceType
)


class TestMemoryOptimization:
    """Test memory optimization features"""
    
    @pytest.mark.asyncio
    async def test_memory_manager_initialization(self):
        """Test memory manager initialization"""
        memory_manager = AdvancedMemoryManager()
        await memory_manager.initialize()
        
        # Check that components are initialized
        assert memory_manager.leak_detector.monitoring_active == True
        assert memory_manager.session_manager is not None
        assert len(memory_manager.gc_thresholds) == 3
        
        await memory_manager.close()
    
    @pytest.mark.asyncio
    async def test_session_memory_management(self):
        """Test session memory management"""
        memory_manager = AdvancedMemoryManager()
        await memory_manager.initialize()
        
        # Register session
        session_id = "test_session_123"
        initial_data = {"key": "value", "timestamp": datetime.utcnow().isoformat()}
        
        await memory_manager.register_session(session_id, initial_data)
        
        # Check session is registered
        assert session_id in memory_manager.session_manager.active_sessions
        assert session_id in memory_manager.session_manager.session_memory_usage
        
        # Update session memory
        large_data = {"large_data": "x" * 1000}  # 1KB of data
        await memory_manager.update_session_memory(session_id, large_data)
        
        # Check memory usage tracking
        assert memory_manager.session_manager.session_memory_usage[session_id] > 0
        
        # Remove session
        await memory_manager.remove_session(session_id)
        assert session_id not in memory_manager.session_manager.active_sessions
        
        await memory_manager.close()
    
    @pytest.mark.asyncio
    async def test_memory_optimization(self):
        """Test forced memory optimization"""
        memory_manager = AdvancedMemoryManager()
        await memory_manager.initialize()
        
        # Create some test sessions
        for i in range(5):
            await memory_manager.register_session(f"session_{i}", {"data": f"test_{i}"})
        
        # Force optimization
        result = await memory_manager.force_optimization()
        
        assert result["status"] == "completed"
        assert "optimization_time" in result
        assert "metrics" in result
        
        await memory_manager.close()
    
    def test_memory_leak_detection(self):
        """Test memory leak detection system"""
        memory_manager = AdvancedMemoryManager()
        
        # Start monitoring
        memory_manager.leak_detector.start_monitoring()
        
        # Take snapshots
        snapshot1 = memory_manager.leak_detector.take_snapshot()
        assert snapshot1 is not None
        
        # Simulate memory growth
        large_objects = []
        for i in range(1000):
            large_objects.append({"data": "x" * 100})  # Create some objects
        
        snapshot2 = memory_manager.leak_detector.take_snapshot()
        assert snapshot2 is not None
        
        # Check for leaks (may not detect any in this simple test)
        leaks = memory_manager.leak_detector.detect_leaks()
        assert isinstance(leaks, list)
        
        memory_manager.leak_detector.stop_monitoring()


class TestAdvancedStateManagement:
    """Test advanced state management features"""
    
    @pytest.mark.asyncio
    async def test_state_manager_initialization(self):
        """Test state manager initialization"""
        state_manager = AdvancedStateManager()
        await state_manager.initialize()
        
        assert state_manager.compression is not None
        assert state_manager.state_cache is not None
        assert state_manager.persistence_level is not None
        
        await state_manager.close()
    
    @pytest.mark.asyncio
    async def test_state_compression(self):
        """Test state compression functionality"""
        state_manager = AdvancedStateManager()
        
        # Test compression
        test_state = {
            "agent_id": "test_agent",
            "session_id": "test_session",
            "data": "x" * 2000,  # 2KB of data
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
        # Test ZLIB compression
        compressed_data, metadata = state_manager.compression.compress_state(
            test_state, StateCompressionType.ZLIB
        )
        
        assert metadata["compressed"] == True
        assert metadata["compression_type"] == "zlib"
        assert metadata["compression_ratio"] > 0
        
        # Test decompression
        decompressed_state = state_manager.compression.decompress_state(compressed_data, metadata)
        assert decompressed_state["agent_id"] == test_state["agent_id"]
        assert decompressed_state["data"] == test_state["data"]
    
    @pytest.mark.asyncio
    async def test_state_storage_retrieval(self):
        """Test state storage and retrieval"""
        state_manager = AdvancedStateManager()
        await state_manager.initialize()
        
        # Store state
        session_id = "test_session"
        agent_id = "test_agent"
        test_state = {
            "step": 1,
            "data": {"key": "value"},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        state_key = await state_manager.store_state(
            session_id, agent_id, test_state, StateCompressionType.ZLIB
        )
        
        assert state_key is not None
        assert state_key in state_manager.state_metadata
        
        # Retrieve state
        retrieved_state = await state_manager.retrieve_state(state_key)
        assert retrieved_state is not None
        assert retrieved_state["step"] == test_state["step"]
        assert retrieved_state["data"] == test_state["data"]
        
        await state_manager.close()
    
    @pytest.mark.asyncio
    async def test_state_transitions(self):
        """Test state transitions"""
        state_manager = AdvancedStateManager()
        await state_manager.initialize()
        
        session_id = "test_session"
        agent_id = "test_agent"
        
        # Initial state
        initial_state = {"step": 1, "status": "starting"}
        initial_key = await state_manager.store_state(session_id, agent_id, initial_state)
        
        # Transition to new state
        new_state = {"step": 2, "status": "processing"}
        new_key = await state_manager.transition_state(session_id, agent_id, initial_key, new_state)
        
        assert new_key != initial_key
        assert len(state_manager.state_transitions) > 0
        
        # Check transition record
        transition = state_manager.state_transitions[-1]
        assert transition.from_state == initial_key
        assert transition.to_state == new_key
        assert transition.agent_id == agent_id
        
        await state_manager.close()
    
    @pytest.mark.asyncio
    async def test_state_cache_performance(self):
        """Test state cache performance"""
        state_manager = AdvancedStateManager()
        
        # Test cache operations
        test_key = "test_cache_key"
        test_data = {"cached": True, "timestamp": datetime.utcnow().isoformat()}
        
        # Set in cache
        await state_manager.state_cache.set(test_key, test_data)
        
        # Get from cache
        cached_data = await state_manager.state_cache.get(test_key)
        assert cached_data is not None
        assert cached_data["cached"] == True
        
        # Check hit rate
        stats = state_manager.state_cache.get_stats()
        assert stats["hit_count"] >= 1
        assert stats["hit_rate"] > 0


class TestAdvancedAgentCoordination:
    """Test advanced agent coordination features"""
    
    @pytest.mark.asyncio
    async def test_coordination_initialization(self):
        """Test coordination system initialization"""
        coordinator = AdvancedAgentCoordinator()
        await coordinator.initialize()
        
        assert coordinator.task_queue is not None
        assert coordinator.resource_manager is not None
        assert coordinator.communication_optimizer is not None
        assert coordinator.max_concurrent_agents > 0
        
        await coordinator.close()
    
    @pytest.mark.asyncio
    async def test_resource_management(self):
        """Test resource allocation and deallocation"""
        coordinator = AdvancedAgentCoordinator()
        
        resources = {
            ResourceType.CPU: 1.0,
            ResourceType.MEMORY: 512.0,
            ResourceType.LLM_TOKENS: 1000,
            ResourceType.DATABASE: 1
        }
        
        instance_id = "test_instance"
        
        # Check if resources can be allocated
        can_allocate = coordinator.resource_manager.can_allocate(instance_id, resources)
        assert can_allocate == True
        
        # Allocate resources
        allocated = coordinator.resource_manager.allocate_resources(instance_id, resources)
        assert allocated == True
        assert instance_id in coordinator.resource_manager.allocated_resources
        
        # Check utilization
        utilization = coordinator.resource_manager.get_utilization()
        assert utilization["cpu"] > 0
        assert utilization["memory"] > 0
        
        # Deallocate resources
        coordinator.resource_manager.deallocate_resources(instance_id)
        assert instance_id not in coordinator.resource_manager.allocated_resources
    
    @pytest.mark.asyncio
    async def test_task_submission_and_queuing(self):
        """Test task submission and queue management"""
        coordinator = AdvancedAgentCoordinator()
        await coordinator.initialize()
        
        # Create test task
        task = AgentTask(
            task_id="test_task_123",
            agent_type="testing",
            description="Test task for coordination",
            priority=AgentPriority.NORMAL,
            session_id="test_session",
            created_at=datetime.utcnow(),
            timeout=60.0,
            dependencies=[],
            resources_required={
                ResourceType.CPU: 0.5,
                ResourceType.MEMORY: 256.0,
                ResourceType.LLM_TOKENS: 500
            },
            metadata={}
        )
        
        # Submit task
        submitted_task_id = await coordinator.submit_task(task)
        assert submitted_task_id == task.task_id
        
        # Check task status
        status = await coordinator.get_task_status(task.task_id)
        assert status["status"] in ["queued", "running"]
        
        # Wait a bit for potential execution
        await asyncio.sleep(0.1)
        
        await coordinator.close()
    
    @pytest.mark.asyncio
    async def test_task_dependencies(self):
        """Test task dependency management"""
        coordinator = AdvancedAgentCoordinator()
        
        # Create tasks with dependencies
        task1 = AgentTask(
            task_id="task_1",
            agent_type="testing",
            description="First task",
            priority=AgentPriority.NORMAL,
            session_id="test_session",
            created_at=datetime.utcnow(),
            timeout=60.0,
            dependencies=[],
            resources_required={ResourceType.CPU: 0.1},
            metadata={}
        )
        
        task2 = AgentTask(
            task_id="task_2",
            agent_type="testing",
            description="Second task",
            priority=AgentPriority.NORMAL,
            session_id="test_session",
            created_at=datetime.utcnow(),
            timeout=60.0,
            dependencies=["task_1"],  # Depends on task_1
            resources_required={ResourceType.CPU: 0.1},
            metadata={}
        )
        
        # Add tasks to queue
        coordinator.task_queue.add_task(task1)
        coordinator.task_queue.add_task(task2)
        
        # Task 1 should be available for execution
        next_task = coordinator.task_queue.get_next_task()
        assert next_task is not None
        assert next_task.task_id == "task_1"
        
        # Task 2 should not be available yet
        next_task = coordinator.task_queue.get_next_task()
        assert next_task is None
        
        # Mark task 1 as completed
        coordinator.task_queue.mark_completed("task_1")
        
        # Now task 2 should be available
        next_task = coordinator.task_queue.get_next_task()
        assert next_task is not None
        assert next_task.task_id == "task_2"
    
    @pytest.mark.asyncio 
    async def test_communication_optimization(self):
        """Test inter-agent communication optimization"""
        coordinator = AdvancedAgentCoordinator()
        
        # Test message sending
        message = {"type": "coordination", "data": "test message"}
        
        result = await coordinator.communication_optimizer.send_message(
            "agent_1", "agent_2", message
        )
        assert result == True
        
        # Check communication stats
        stats = coordinator.communication_optimizer.get_communication_stats()
        assert stats["messages_sent"] >= 1
        assert "avg_latency_ms" in stats


class TestIntegrationWorkflow:
    """Test integration between all Sprint 2.1 components"""
    
    @pytest.mark.asyncio
    async def test_full_integration_workflow(self):
        """Test full integration workflow with all components"""
        # Initialize all components
        memory_manager = AdvancedMemoryManager()
        state_manager = AdvancedStateManager()
        coordinator = AdvancedAgentCoordinator()
        
        await memory_manager.initialize()
        await state_manager.initialize()
        await coordinator.initialize()
        
        try:
            # 1. Register session in memory manager
            session_id = "integration_test_session"
            await memory_manager.register_session(session_id, {"workflow": "integration_test"})
            
            # 2. Store initial state
            initial_state = {
                "workflow_step": 1,
                "status": "started",
                "data": {"test": True}
            }
            state_key = await state_manager.store_state(
                session_id, "test_agent", initial_state, StateCompressionType.ZLIB
            )
            
            # 3. Submit coordinated task
            task = AgentTask(
                task_id="integration_test_task",
                agent_type="testing",
                description="Integration test task",
                priority=AgentPriority.HIGH,
                session_id=session_id,
                created_at=datetime.utcnow(),
                timeout=30.0,
                dependencies=[],
                resources_required={
                    ResourceType.CPU: 0.2,
                    ResourceType.MEMORY: 128.0
                },
                metadata={"state_key": state_key}
            )
            
            task_id = await coordinator.submit_task(task)
            
            # 4. Wait for task processing
            await asyncio.sleep(0.5)
            
            # 5. Check task status
            task_status = await coordinator.get_task_status(task_id)
            assert task_status["status"] in ["queued", "running", "completed"]
            
            # 6. Transition state
            new_state = {
                "workflow_step": 2,
                "status": "processing",
                "data": {"test": True, "processed": True}
            }
            new_state_key = await state_manager.transition_state(
                session_id, "test_agent", state_key, new_state
            )
            
            # 7. Get metrics from all components
            memory_metrics = memory_manager.get_memory_metrics()
            state_metrics = state_manager.get_state_metrics()
            coordination_metrics = coordinator.get_coordination_metrics()
            
            # Verify integration
            assert "system" in memory_metrics
            assert "current" in state_metrics
            assert "current" in coordination_metrics
            
            # Verify session exists across components
            assert session_id in memory_manager.session_manager.active_sessions
            assert len(state_manager.state_transitions) > 0
            
        finally:
            # Cleanup
            await coordinator.close()
            await state_manager.close()
            await memory_manager.close()
    
    @pytest.mark.asyncio
    async def test_performance_under_load(self):
        """Test performance under simulated load"""
        memory_manager = AdvancedMemoryManager()
        state_manager = AdvancedStateManager()
        coordinator = AdvancedAgentCoordinator()
        
        await memory_manager.initialize()
        await state_manager.initialize()
        await coordinator.initialize()
        
        try:
            start_time = datetime.utcnow()
            
            # Create multiple sessions and tasks
            tasks = []
            for i in range(10):
                session_id = f"load_test_session_{i}"
                
                # Register session
                await memory_manager.register_session(session_id, {"load_test": i})
                
                # Store state
                state = {"iteration": i, "data": "x" * 100}  # Some data
                state_key = await state_manager.store_state(
                    session_id, f"agent_{i}", state
                )
                
                # Create task
                task = AgentTask(
                    task_id=f"load_test_task_{i}",
                    agent_type="testing",
                    description=f"Load test task {i}",
                    priority=AgentPriority.NORMAL,
                    session_id=session_id,
                    created_at=datetime.utcnow(),
                    timeout=30.0,
                    dependencies=[],
                    resources_required={ResourceType.CPU: 0.1},
                    metadata={}
                )
                
                tasks.append(coordinator.submit_task(task))
            
            # Wait for all tasks to be submitted
            submitted_tasks = await asyncio.gather(*tasks)
            assert len(submitted_tasks) == 10
            
            # Wait for processing
            await asyncio.sleep(1.0)
            
            # Check final metrics
            memory_metrics = memory_manager.get_memory_metrics()
            state_metrics = state_manager.get_state_metrics()
            coordination_metrics = coordinator.get_coordination_metrics()
            
            end_time = datetime.utcnow()
            test_duration = (end_time - start_time).total_seconds()
            
            # Performance assertions
            assert test_duration < 5.0  # Should complete within 5 seconds
            assert memory_metrics["sessions"]["active_sessions"] >= 10
            assert state_metrics["current"]["total_states"] >= 10
            
        finally:
            await coordinator.close()
            await state_manager.close()
            await memory_manager.close()


# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmarks for Sprint 2.1 components"""
    
    @pytest.mark.asyncio
    async def test_memory_optimization_performance(self):
        """Benchmark memory optimization performance"""
        memory_manager = AdvancedMemoryManager()
        await memory_manager.initialize()
        
        # Create many sessions
        start_time = datetime.utcnow()
        
        for i in range(100):
            await memory_manager.register_session(f"perf_session_{i}", {"data": f"test_{i}"})
        
        # Force optimization
        optimization_result = await memory_manager.force_optimization()
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Performance assertions
        assert duration < 2.0  # Should complete within 2 seconds
        assert optimization_result["status"] == "completed"
        
        await memory_manager.close()
    
    @pytest.mark.asyncio
    async def test_state_compression_performance(self):
        """Benchmark state compression performance"""
        state_manager = AdvancedStateManager()
        
        # Create large state
        large_state = {
            "data": "x" * 10000,  # 10KB of data
            "metadata": {"items": [{"id": i, "value": f"item_{i}"} for i in range(100)]}
        }
        
        start_time = datetime.utcnow()
        
        # Compress and decompress 50 times
        for _ in range(50):
            compressed_data, metadata = state_manager.compression.compress_state(
                large_state, StateCompressionType.ZLIB
            )
            decompressed_state = state_manager.compression.decompress_state(
                compressed_data, metadata
            )
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Performance assertions
        assert duration < 1.0  # Should complete within 1 second
        assert decompressed_state["data"] == large_state["data"]
    
    @pytest.mark.asyncio
    async def test_coordination_throughput(self):
        """Benchmark coordination throughput"""
        coordinator = AdvancedAgentCoordinator()
        await coordinator.initialize()
        
        start_time = datetime.utcnow()
        
        # Submit many tasks quickly
        tasks = []
        for i in range(50):
            task = AgentTask(
                task_id=f"throughput_task_{i}",
                agent_type="testing",
                description=f"Throughput test {i}",
                priority=AgentPriority.NORMAL,
                session_id=f"throughput_session_{i}",
                created_at=datetime.utcnow(),
                timeout=30.0,
                dependencies=[],
                resources_required={ResourceType.CPU: 0.05},
                metadata={}
            )
            tasks.append(coordinator.submit_task(task))
        
        # Wait for all submissions
        await asyncio.gather(*tasks)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Calculate throughput
        throughput = 50 / duration  # tasks per second
        
        # Performance assertions
        assert throughput > 20  # Should handle >20 tasks/second
        assert duration < 3.0   # Should complete within 3 seconds
        
        await coordinator.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
