from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import wraps
from time import time
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager


class ArgumentProvider(metaclass=ABCMeta):
    throw_if_not_present: bool

    def __init__(self, throw_if_not_present: bool = False):
        self.throw_if_not_present = throw_if_not_present

    @abstractmethod
    def get_parameter(self, *args, **kwargs) -> Tuple[str, Any]:
        pass


class PositionalArgumentProvider(ArgumentProvider):
    position: int
    alias: str

    throw_if_not_present: bool

    def __init__(self, position: int, alias: str, throw_if_not_present: bool = False):
        super(PositionalArgumentProvider, self).__init__(throw_if_not_present)
        self.position = position
        self.alias = alias

    def get_parameter(self, *args, **kwargs) -> Tuple[str, Any]:
        if len(args) <= self.position:
            if self.throw_if_not_present:
                raise IndexError(f"Function was called with less then {self.position + 1} argument.")
            return self.alias, None
        return self.alias, args[self.position]


class KeywordArgumentProvider(ArgumentProvider):
    key: str

    throw_if_not_present: bool

    def __init__(self, key: str, throw_if_not_present: bool = False):
        super(KeywordArgumentProvider, self).__init__(throw_if_not_present)
        self.key = key

    def get_parameter(self, *args, **kwargs) -> Tuple[str, Any]:
        if self.key not in kwargs:
            if self.throw_if_not_present:
                raise IndexError(f"Function was called with no {self.key} keyword argument.")
            return self.key, None
        return self.key, kwargs[self.key]


@dataclass
class CallStackEntry:
    function_name: str
    execution_time: Optional[float]
    called_from_stack: List[str]
    saved_arguments: Optional[Dict[str, Any]]


class Session:
    call_stack: List[CallStackEntry]

    def __init__(self):
        self.call_stack = []

    def add_call(self, entry: CallStackEntry):
        self.call_stack.append(entry)

    def __str__(self):
        return str(self.call_stack)

    def __repr__(self):
        return "Session(" + str(self.call_stack) + ")"


class Profiler:
    scopes: Dict[str, List[Session]]

    scoped_active_functions: Dict[str, List[str]]

    def __init__(self):
        self.scopes = {}
        self.scoped_active_functions = {}

    def _get_active_session(self, scope_name: str):
        return self.scopes[scope_name][-1]

    def scope_controller(self, scope_name: str, profile: bool = True):
        def wrapper(func):
            if scope_name not in self.scopes:
                self.scopes[scope_name] = []
                self.scoped_active_functions[scope_name] = []
            if profile:
                func = self.profile(scope_name)(func)

            @wraps(func)
            def internal(*args, **kwargs):
                self.scopes[scope_name].append(Session())
                return func(*args, **kwargs)

            return internal

        return wrapper

    def profile(
            self,
            scope_name: str,
            remember_arguments: List[ArgumentProvider] = None
    ):
        def wrapper(func):
            @wraps(func)
            def internal(*args, **kwargs):
                entry = CallStackEntry(
                    function_name=func.__name__,
                    execution_time=None,
                    called_from_stack=list(self.scoped_active_functions[scope_name]),
                    saved_arguments=None
                )
                self.scoped_active_functions[scope_name].append(func.__name__)
                self._get_active_session(scope_name).add_call(entry)

                if remember_arguments:
                    entry.saved_arguments = dict(
                        [provider.get_parameter(*args, **kwargs) for provider in remember_arguments])

                start = time()
                result = func(*args, **kwargs)
                entry.execution_time = time() - start

                self.scoped_active_functions[scope_name].pop()
                return result

            return internal

        return wrapper

    @contextmanager
    def profile_code(self, scope_name: str, code_name: str):
        entry = CallStackEntry(
            function_name=code_name,
            execution_time=None,
            called_from_stack=list(self.scoped_active_functions[scope_name]),
            saved_arguments=None
        )
        self.scoped_active_functions[scope_name].append(code_name)
        self._get_active_session(scope_name).add_call(entry)

        start = time()
        yield
        entry.execution_time = time() - start

        self.scoped_active_functions[scope_name].pop()

    def get_result_and_clean(self):
        scopes = self.scopes
        self.scopes = {scope: [] for scope in scopes}
        self.scoped_active_functions = {}
        return scopes

    def visualize_detailed(self, scopes: dict, indent: int = 1, max_depth: int = 2):
        if not scopes:
            scopes = self.scopes.items()
        for scope, sessions in scopes.items():
            print(f"=== Scope '{scope}' ===")
            for i, session in enumerate(sessions):
                print(f"- Session {i} -")
                for entry in session.call_stack:
                    if len(entry.called_from_stack) > max_depth:
                        continue
                    print(
                        " " * indent * len(entry.called_from_stack) +
                        f"{entry.function_name}: {entry.execution_time:.9f}s | {entry.saved_arguments}"
                    )

    def visualize_aggregated(self, scopes: dict = None):
        if not scopes:
            scopes = self.scopes.items()
        for scope, sessions in scopes:
            print(f"=== Scope '{scope}' ===")

            grouped_data = {}

            for session in sessions:
                for entry in session.call_stack:

                    if entry.function_name in grouped_data:
                        grouped_data[entry.function_name].append(entry.execution_time)
                    else:
                        grouped_data[entry.function_name] = [entry.execution_time]

            for function, execution_time_entries in grouped_data.items():
                print(f"--- {function} ---")
                print(f"called:")
                print(f"    count({len(execution_time_entries):.9f})")
                print(f"    avg({len(execution_time_entries) / len(sessions)})/session")
                print(f"execution time")
                print(f"    sum({sum(execution_time_entries):.9f})")
                print(f"    avg({sum(execution_time_entries) / len(sessions):.9f})/session")
                print(f"    avg({sum(execution_time_entries) / len(execution_time_entries):.9f})/call")
                print()

