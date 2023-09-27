import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class InferenceRuleArguments:
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class Test(InferenceRuleArguments):
    x: int
    y: int


t = Test(x=1, y=2)
print(t)
print(type(t))
print(type(Test))
