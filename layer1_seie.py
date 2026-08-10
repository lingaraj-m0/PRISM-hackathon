import json
import hashlib
import math
from typing import Dict
from collections import OrderedDict

class SymbolicEntityInterningEngine:
    def __init__(self, max_cache_size: int = 10000, entropy_threshold: float = 4.8):
        # Upgraded to OrderedDict for LRU eviction
        self._cas_heap: OrderedDict[str, memoryview] = OrderedDict()
        self.metrics = {
            "raw_bytes": 0, 
            "interned_bytes": 0, 
            "pointers_allocated": 0, 
            "blocked_anomalies": 0
        }
        self.MAX_CACHE_SIZE = max_cache_size
        self.ENTROPY_THRESHOLD = entropy_threshold

    def _compute_structural_hash(self, payload: dict) -> str:
        canonical_str = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(canonical_str).hexdigest()[:12]

    def _calculate_shannon_entropy(self, data_str: str) -> float:
        """Calculates the Shannon entropy to detect highly randomized DDoS payloads."""
        if not data_str:
            return 0.0
        prob = [float(data_str.count(c)) / len(data_str) for c in dict.fromkeys(list(data_str))]
        entropy = -sum(p * math.log2(p) for p in prob)
        return entropy

    def process_telemetry_stream(self, raw_log: dict) -> str:
        raw_bytes = len(json.dumps(raw_log).encode('utf-8'))
        self.metrics["raw_bytes"] += raw_bytes
        
        # 1. Pre-Ingress Entropy Circuit Breaker
        payload_str = json.dumps(raw_log)
        entropy = self._calculate_shannon_entropy(payload_str)
        
        if entropy > self.ENTROPY_THRESHOLD:
            self.metrics["blocked_anomalies"] += 1
            return f"[CIRCUIT_BREAKER_TRIPPED | ENTROPY: {round(entropy, 2)} | REJECTED: DDoS Anomaly]"

        event_type = raw_log.get("eventName", "UNKNOWN_ANOMALY")
        src_ip = raw_log.get("sourceIPAddress", "0.0.0.0")
        cas_ptr = self._compute_structural_hash(raw_log)

        # 2. OOM Protection: Bounded Cache Eviction (LRU)
        if cas_ptr not in self._cas_heap:
            if len(self._cas_heap) >= self.MAX_CACHE_SIZE:
                # Evict the Least Recently Used item to prevent memory thrashing
                self._cas_heap.popitem(last=False)
                self.metrics["pointers_allocated"] -= 1
                
            self._cas_heap[cas_ptr] = memoryview(json.dumps(raw_log).encode('utf-8'))
            self.metrics["pointers_allocated"] += 1
        else:
            # Move to end to mark as recently used
            self._cas_heap.move_to_end(cas_ptr)

        symbolic_handle = f"[MEM_PTR: 0x{cas_ptr.upper()} | ENCLAVE: {event_type} | ADDR: {src_ip}]"
        self.metrics["interned_bytes"] += len(symbolic_handle.encode('utf-8'))
        return symbolic_handle

    def yield_compression_ratio(self) -> dict:
        raw = max(1, self.metrics["raw_bytes"])
        interned = max(1, self.metrics["interned_bytes"])
        return {
            "compression_factor": round(raw / interned, 2),
            "token_savings_pct": round((1 - (interned / raw)) * 100, 4),
            "active_pointers": self.metrics["pointers_allocated"],
            "blocked_anomalies": self.metrics["blocked_anomalies"]
        }