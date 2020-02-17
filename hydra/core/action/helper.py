
class ActionPattern(str):
    def __init__(self, pattern):
        super().__init__(pattern)

    def __contains__(self, item):
        if isinstance(item, str):
            return action_cmp(item, self.__str__())
        return False


def action_cmp(action_type: str, pattern: str):
    """
    Compares the start of action_type with the pattern

    Example:
    ```
    action_cmp("event.node.close", "event.node") == True
    action_cmp("event.node.close", "event.group") == False
    action_cmp("event.node.close", "{2}.close") == True
    action_cmp("event.node.close", "event.node|group") == True
    action_cmp("event.node.close", "event.(node.close)|group") == True
    action_cmp("event.node.close", "event.(node|group).close") == True
    action_cmp("event.node.close", "event.!(node|group).close") == False
    ```
    Patterns:
    * - anything
    {n} - any n dot seperated subtypes
    {*} - any dot seperated subtypes
    | - or operator
    ! - not operator
    () - group operator
    """

    #TODO: Impl
    return action_type.startswith(pattern)
