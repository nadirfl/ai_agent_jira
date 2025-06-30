import importlib
import pkgutil
import tools

def load_tools(usage_filter=None):
    registry = {}
    for _, name, _ in pkgutil.iter_modules(tools.__path__):
        module = importlib.import_module(f"tools.{name}")
        if not hasattr(module, "run"):
            continue

        usage = getattr(module, "TOOL_USAGE", "ALL")
        if usage_filter is None or usage_filter in usage or usage == "ALL":
            key = getattr(module, "TOOL_NAME", name)
            registry[key] = {
                "run": module.run,
                "name": getattr(module, "TOOL_NAME", name),
                "desc": getattr(module, "TOOL_DESC", "Kein Beschreibungstext"),
                "usage": usage
            }
    return registry