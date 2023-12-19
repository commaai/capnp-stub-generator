import dummy_capnp

assert dummy_capnp.TestEnum is not None
assert dummy_capnp.TestEnum.foo == 0
assert dummy_capnp.TestEnum.bar == 1

assert dummy_capnp.TestMap is not None

test_map = dummy_capnp.TestMap.new_message()

text_map = test_map.init("textMap")

assert test_map.textMap is not None

text_entries = text_map.init_resizable_list("entries")
text_entry = text_entries.add()
text_entry.key = "foo"
text_entry.value = "123"
