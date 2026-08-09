import logging
import time

# Configure structured logging for the orchestrator
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("DSOE_Saga")

def forward_action(host_id: str) -> None:
    """Executes the primary security action."""
    logger.info(f"[EXECUTE] Isolating Host: {host_id}.")
    # Simulate network delay/execution time
    time.sleep(1)

def compensating_action(host_id: str) -> None:
    """Reverts the primary security action if the workflow fails."""
    logger.info(f"[SAGA ROLLBACK] Unisolating Host: {host_id}.")
    # Simulate network delay/execution time
    time.sleep(1)

def execute_saga_workflow(host_id: str) -> None:
    """
    Orchestrates the transactional execution of a security action.
    Includes built-in error simulation to trigger the compensation logic.
    """
    logger.info(f"--- Starting Saga Transaction for target: {host_id} ---")
    
    try:
        # 1. Execute the forward action
        forward_action(host_id)
        
        # 2. Simulate a failure (e.g., API timeout, false positive alert, DLME block)
        logger.warning("[SIMULATION] Exception encountered: False positive detected after isolation.")
        raise RuntimeError("Operation aborted due to policy conflict.")
        
        # (If successful, this would log completion)
        logger.info(f"[SUCCESS] Workflow completed for {host_id}.")
        
    except Exception as e:
        # 3. Catch the failure and trigger the rollback
        logger.error(f"[FAILED] Transaction interrupted: {e}")
        logger.info("Initiating sequential Saga compensation...")
        
        try:
            compensating_action(host_id)
            logger.info("--- Saga Rollback Completed Successfully ---")
        except Exception as rollback_error:
            # In a production system, a failed rollback requires human intervention
            logger.critical(f"[FATAL] Saga compensation failed: {rollback_error}")

if __name__ == "__main__":
    # Test the workflow with the target IP
    target_ip = "192.168.1.50"
    execute_saga_workflow(target_ip)