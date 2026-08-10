import time

class DurableSagaOrchestrationEngine:
    def __init__(self):
        self.execution_dag = []
        self.compensating_dag = []
        self.audit_ledger = []

    def register_transaction(self, forward_op: str, reverse_op: str):
        self.execution_dag.append(forward_op)
        self.compensating_dag.insert(0, reverse_op)

    def execute_speculative_branch(self, target: str):
        self.audit_ledger.clear()
        self.execution_dag.clear()
        self.compensating_dag.clear()
        
        self.audit_ledger.append(f"[T=0] Initializing Speculative Micro-VM Sandbox for {target}")
        self.register_transaction(f"Isolate_EC2_Instance({target})", f"Restore_EC2_Instance({target})")
        self.register_transaction(f"Revoke_IAM_Role({target})", f"Reattach_IAM_Role({target})")

        for op in self.execution_dag:
            self.audit_ledger.append(f"[FORWARD_MUTATION] ➔ {op}")
            time.sleep(0.3)

        self.audit_ledger.append("[EPISTEMIC FAULT] False Positive Detected! Target is critical infrastructure.")
        return self._trigger_acid_rollback()

    def _trigger_acid_rollback(self):
        self.audit_ledger.append("==================================================")
        self.audit_ledger.append("[INITIATING DURABLE SAGA ROLLBACK]")
        self.audit_ledger.append("==================================================")
        
        MAX_RETRIES = 3
        
        for comp_op in self.compensating_dag:
            success = False
            for attempt in range(MAX_RETRIES):
                try:
                    self.audit_ledger.append(f"[COMPENSATING_TRANSACTION] ↺ Attempt {attempt + 1}: {comp_op}")
                    
                    # Simulating the actual API call execution
                    time.sleep(0.4) 
                    
                    success = True
                    break # Exit retry loop on success
                    
                except Exception as e:
                    backoff_time = 2 ** attempt
                    self.audit_ledger.append(f"[WARNING] Compensating action failed: {e}. Retrying in {backoff_time}s...")
                    time.sleep(backoff_time)
            
            if not success:
                # Deadlock Protection: Route to Dead Letter Queue
                self.audit_ledger.append(f"[FATAL] Transaction '{comp_op}' permanently failed. Routing to DLQ.")
                self.audit_ledger.append("[SYSTEM HALT] Manual Human Intervention Required. System Partitioned.")
                return self.audit_ledger
            
        self.audit_ledger.append("[STATE ALIGNMENT] Core enterprise memory restored to pristine baseline.")
        return self.audit_ledger