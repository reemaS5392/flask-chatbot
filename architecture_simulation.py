"""Simple simulation for the Flask chatbot system architecture.

The simulation models the main components of this project:
- Client UI (browser)
- Flask API layer
- Response Router (predefined vs OpenAI)
- OpenAI service (fallback)

Usage:
    python architecture_simulation.py --requests 20 --seed 42
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from statistics import mean
from typing import List, Tuple

PREDEFINED_QUESTIONS = [
    "which courses offered?",
    "where are the institute located?",
    "what is the duration of the degrees?",
    "how many faculties?",
]

OPENAI_QUESTIONS = [
    "tell me about scholarship opportunities",
    "what are admission requirements for international students",
    "can you explain registration deadlines",
    "which departments have research labs",
]


@dataclass
class RequestResult:
    request_id: int
    route: str
    latency_ms: float
    success: bool


class Component:
    def __init__(self, name: str, min_latency_ms: float, max_latency_ms: float) -> None:
        self.name = name
        self.min_latency_ms = min_latency_ms
        self.max_latency_ms = max_latency_ms

    def process(self) -> float:
        """Return simulated latency for this component in milliseconds."""
        return random.uniform(self.min_latency_ms, self.max_latency_ms)


class ArchitectureSimulation:
    def __init__(
        self,
        openai_failure_rate: float = 0.08,
        predefined_ratio: float = 0.55,
    ) -> None:
        self.openai_failure_rate = openai_failure_rate
        self.predefined_ratio = predefined_ratio

        self.client = Component("Client UI", 5, 20)
        self.flask_api = Component("Flask API", 8, 35)
        self.router = Component("Response Router", 1, 5)
        self.predefined_engine = Component("Predefined Response Engine", 1, 4)
        self.openai_service = Component("OpenAI API", 250, 900)

    def _simulate_single(self, request_id: int) -> Tuple[str, float, bool]:
        total_latency = 0.0

        # Client sends request
        total_latency += self.client.process()
        total_latency += self.flask_api.process()
        total_latency += self.router.process()

        use_predefined = random.random() < self.predefined_ratio

        if use_predefined:
            _ = random.choice(PREDEFINED_QUESTIONS)
            total_latency += self.predefined_engine.process()
            return "predefined", total_latency, True

        _ = random.choice(OPENAI_QUESTIONS)
        total_latency += self.openai_service.process()
        success = random.random() > self.openai_failure_rate
        return "openai", total_latency, success

    def run(self, request_count: int) -> List[RequestResult]:
        results: List[RequestResult] = []

        for i in range(1, request_count + 1):
            route, latency, success = self._simulate_single(i)
            results.append(
                RequestResult(
                    request_id=i,
                    route=route,
                    latency_ms=latency,
                    success=success,
                )
            )

        return results


def print_report(results: List[RequestResult]) -> None:
    total = len(results)
    predefined = [r for r in results if r.route == "predefined"]
    openai = [r for r in results if r.route == "openai"]

    failures = [r for r in results if not r.success]
    avg_latency = mean(r.latency_ms for r in results) if results else 0

    print("\n=== System Architecture Simulation Report ===")
    print(f"Total requests: {total}")
    print(f"Predefined route: {len(predefined)} ({len(predefined)/total:.1%})" if total else "Predefined route: 0")
    print(f"OpenAI route: {len(openai)} ({len(openai)/total:.1%})" if total else "OpenAI route: 0")
    print(f"Overall success rate: {(total - len(failures))/total:.1%}" if total else "Overall success rate: 0%")
    print(f"Average end-to-end latency: {avg_latency:.2f} ms")

    if openai:
        print(f"Average OpenAI-route latency: {mean(r.latency_ms for r in openai):.2f} ms")
    if predefined:
        print(f"Average predefined-route latency: {mean(r.latency_ms for r in predefined):.2f} ms")

    if failures:
        print("\nFailed request IDs:", ", ".join(str(r.request_id) for r in failures))

    print("\nSample trace (first 10 requests):")
    for row in results[:10]:
        status = "OK" if row.success else "FAIL"
        print(
            f"- Request #{row.request_id:03d} | route={row.route:10s} | "
            f"latency={row.latency_ms:7.2f} ms | {status}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate chatbot system architecture behavior.")
    parser.add_argument("--requests", type=int, default=50, help="Number of simulated requests.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducible runs.")
    parser.add_argument(
        "--openai-failure-rate",
        type=float,
        default=0.08,
        help="Probability of failure when request goes to OpenAI route.",
    )
    parser.add_argument(
        "--predefined-ratio",
        type=float,
        default=0.55,
        help="Probability of routing to predefined response path.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    random.seed(args.seed)

    simulation = ArchitectureSimulation(
        openai_failure_rate=args.openai_failure_rate,
        predefined_ratio=args.predefined_ratio,
    )
    report = simulation.run(args.requests)
    print_report(report)
