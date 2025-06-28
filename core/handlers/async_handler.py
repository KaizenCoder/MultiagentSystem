#!/usr/bin/env python3
"""
Handler pour le logging asynchrone non-bloquant.
"""

import logging
from queue import Queue, Empty
import threading
from typing import Dict, List

# Constantes pour le handler asynchrone
ASYNC_QUEUE_SIZE = 10000
ASYNC_BATCH_SIZE = 200
ASYNC_FLUSH_INTERVAL = 0.5

class CompositeHandler(logging.Handler):
    """Un handler qui propage les enregistrements à plusieurs handlers de base."""
    def __init__(self, handlers: List[logging.Handler]):
        super().__init__()
        self.handlers = handlers

    def emit(self, record):
        for handler in self.handlers:
            handler.handle(record)

    def close(self):
        for handler in self.handlers:
            if hasattr(handler, 'close'):
                handler.close()
        super().close()

class AsyncLogHandler(logging.Handler):
    """
    Un handler qui place les enregistrements de log dans une file d'attente
    et les traite dans un thread séparé pour ne pas bloquer l'application.
    """
    
    def __init__(self, base_handler: logging.Handler, queue_size: int = ASYNC_QUEUE_SIZE, 
                 batch_size: int = ASYNC_BATCH_SIZE, flush_interval: float = ASYNC_FLUSH_INTERVAL):
        super().__init__()
        self.base_handler = base_handler
        self.queue = Queue(queue_size)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def _worker(self):
        """Le worker qui consomme les logs depuis la file d'attente."""
        while True:
            batch = []
            try:
                # Remplir un batch
                while len(batch) < self.batch_size:
                    timeout = self.flush_interval if not batch else None
                    record = self.queue.get(block=True, timeout=timeout)
                    if record is None: # Signal de terminaison
                        if batch:
                            self._flush_batch(batch)
                        return
                    batch.append(record)
                
                if batch:
                    self._flush_batch(batch)

            except Empty:
                if batch:
                    self._flush_batch(batch)

    def _flush_batch(self, batch):
        """Traite un batch d'enregistrements de log."""
        for record in batch:
            try:
                self.base_handler.handle(record)
            except Exception:
                # En cas d'erreur dans le handler de base, on ne peut pas faire grand chose
                # à part l'ignorer pour ne pas crasher le worker.
                pass

    def emit(self, record):
        """Place un enregistrement dans la file d'attente."""
        try:
            self.queue.put_nowait(record)
        except Exception:
            # La file est pleine, on ignore le message de log
            self.handleError(record)

    def close(self):
        """Termine le handler proprement."""
        self.queue.put(None) # Signal de fin
        self._worker_thread.join()
        super().close()
        if hasattr(self.base_handler, 'close'):
            self.base_handler.close() 



