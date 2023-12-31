# Copyright (c) 2013-2014 Sandstorm Development Group, Inc. and contributors
# Licensed under the MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

@0xd6fe35252d9d2bbb;

using C = import "c.capnp";
using Cxx = import "c++.capnp";

$C.fieldgetset;

# Use a namespace likely to cause trouble if the generated code doesn't use fully-qualified
# names for stuff in the capnproto namespace.
$Cxx.namespace("capnproto_test::capnp::test");

enum TestEnum {
  foo @0;
  bar @1;
  baz @2;
  qux @3;
  quux @4;
  corge @5;
  grault @6;
  garply @7;
}

struct TestAllTypes {
  voidField      @0  : Void;
  boolField      @1  : Bool;
  int8Field      @2  : Int8;
  int16Field     @3  : Int16;
  int32Field     @4  : Int32;
  int64Field     @5  : Int64;
  uInt8Field     @6  : UInt8;
  uInt16Field    @7  : UInt16;
  uInt32Field    @8  : UInt32;
  uInt64Field    @9  : UInt64;
  float32Field   @10 : Float32;
  float64Field   @11 : Float64;
  textField      @12 : Text;
  dataField      @13 : Data;
  structField    @14 : TestAllTypes;
  enumField      @15 : TestEnum;
  interfaceField @16 : Void;  # TODO

  voidList      @17 : List(Void);
  boolList      @18 : List(Bool);
  int8List      @19 : List(Int8);
  int16List     @20 : List(Int16);
  int32List     @21 : List(Int32);
  int64List     @22 : List(Int64);
  uInt8List     @23 : List(UInt8);
  uInt16List    @24 : List(UInt16);
  uInt32List    @25 : List(UInt32);
  uInt64List    @26 : List(UInt64);
  float32List   @27 : List(Float32);
  float64List   @28 : List(Float64);
  textList      @29 : List(Text);
  dataList      @30 : List(Data);
  structList    @31 : List(TestAllTypes);
  enumList      @32 : List(TestEnum);
  interfaceList @33 : List(Void);  # TODO
}

struct TestDefaults {
  voidField      @0  : Void    = void;
  boolField      @1  : Bool    = true;
  int8Field      @2  : Int8    = -123;
  int16Field     @3  : Int16   = -12345;
  int32Field     @4  : Int32   = -12345678;
  int64Field     @5  : Int64   = -123456789012345;
  uInt8Field     @6  : UInt8   = 234;
  uInt16Field    @7  : UInt16  = 45678;
  uInt32Field    @8  : UInt32  = 3456789012;
  uInt64Field    @9  : UInt64  = 12345678901234567890;
  float32Field   @10 : Float32 = 1234.5;
  float64Field   @11 : Float64 = -123e45;
  textField      @12 : Text    = "foo";
  dataField      @13 : Data    = 0x"62 61 72"; # "bar"
  structField    @14 : TestAllTypes = (
      voidField      = void,
      boolField      = true,
      int8Field      = -12,
      int16Field     = 3456,
      int32Field     = -78901234,
      int64Field     = 56789012345678,
      uInt8Field     = 90,
      uInt16Field    = 1234,
      uInt32Field    = 56789012,
      uInt64Field    = 345678901234567890,
      float32Field   = -1.25e-10,
      float64Field   = 345,
      textField      = "baz",
      dataField      = "qux",
      structField    = (
          textField = "nested",
          structField = (textField = "really nested")),
      enumField      = baz,
      # interfaceField can't have a default

      voidList      = [void, void, void],
      boolList      = [false, true, false, true, true],
      int8List      = [12, -34, -0x80, 0x7f],
      int16List     = [1234, -5678, -0x8000, 0x7fff],
      int32List     = [12345678, -90123456, -0x80000000, 0x7fffffff],
      int64List     = [123456789012345, -678901234567890, -0x8000000000000000, 0x7fffffffffffffff],
      uInt8List     = [12, 34, 0, 0xff],
      uInt16List    = [1234, 5678, 0, 0xffff],
      uInt32List    = [12345678, 90123456, 0, 0xffffffff],
      uInt64List    = [123456789012345, 678901234567890, 0, 0xffffffffffffffff],
      float32List   = [0, 1234567, 1e37, -1e37, 1e-37, -1e-37],
      float64List   = [0, 123456789012345, 1e306, -1e306, 1e-306, -1e-306],
      textList      = ["quux", "corge", "grault"],
      dataList      = ["garply", "waldo", "fred"],
      structList    = [
          (textField = "x structlist 1"),
          (textField = "x structlist 2"),
          (textField = "x structlist 3")],
      enumList      = [qux, bar, grault]
      # interfaceList can't have a default
      );
  enumField      @15 : TestEnum = corge;
  interfaceField @16 : Void;  # TODO

  voidList      @17 : List(Void)    = [void, void, void, void, void, void];
  boolList      @18 : List(Bool)    = [true, false, false, true];
  int8List      @19 : List(Int8)    = [111, -111];
  int16List     @20 : List(Int16)   = [11111, -11111];
  int32List     @21 : List(Int32)   = [111111111, -111111111];
  int64List     @22 : List(Int64)   = [1111111111111111111, -1111111111111111111];
  uInt8List     @23 : List(UInt8)   = [111, 222] ;
  uInt16List    @24 : List(UInt16)  = [33333, 44444];
  uInt32List    @25 : List(UInt32)  = [3333333333];
  uInt64List    @26 : List(UInt64)  = [11111111111111111111];
  float32List   @27 : List(Float32) = [5555.5, inf, -inf, nan];
  float64List   @28 : List(Float64) = [7777.75, inf, -inf, nan];
  textList      @29 : List(Text)    = ["plugh", "xyzzy", "thud"];
  dataList      @30 : List(Data)    = ["oops", "exhausted", "rfc3092"];
  structList    @31 : List(TestAllTypes) = [
      (textField = "structlist 1"),
      (textField = "structlist 2"),
      (textField = "structlist 3")];
  enumList      @32 : List(TestEnum) = [foo, garply];
  interfaceList @33 : List(Void);  # TODO
}

struct TestAnyPointer {
  anyPointerField @0 :AnyPointer;

  # Do not add any other fields here!  Some tests rely on anyPointerField being the last pointer
  # in the struct.
}

struct TestOutOfOrder {
  foo @3 :Text;
  bar @2 :Text;
  baz @8 :Text;
  qux @0 :Text;
  quux @6 :Text;
  corge @4 :Text;
  grault @1 :Text;
  garply @7 :Text;
  waldo @5 :Text;
}

struct TestUnion {
  union0 @0! :union {
    # Pack union 0 under ideal conditions: there is no unused padding space prior to it.
    u0f0s0  @4: Void;
    u0f0s1  @5: Bool;
    u0f0s8  @6: Int8;
    u0f0s16 @7: Int16;
    u0f0s32 @8: Int32;
    u0f0s64 @9: Int64;
    u0f0sp  @10: Text;

    # Pack more stuff into union0 -- should go in same space.
    u0f1s0  @11: Void;
    u0f1s1  @12: Bool;
    u0f1s8  @13: Int8;
    u0f1s16 @14: Int16;
    u0f1s32 @15: Int32;
    u0f1s64 @16: Int64;
    u0f1sp  @17: Text;
  }

  # Pack one bit in order to make pathological situation for union1.
  bit0 @18: Bool;

  union1 @1! :union {
    # Pack pathologically bad case.  Each field takes up new space.
    u1f0s0  @19: Void;
    u1f0s1  @20: Bool;
    u1f1s1  @21: Bool;
    u1f0s8  @22: Int8;
    u1f1s8  @23: Int8;
    u1f0s16 @24: Int16;
    u1f1s16 @25: Int16;
    u1f0s32 @26: Int32;
    u1f1s32 @27: Int32;
    u1f0s64 @28: Int64;
    u1f1s64 @29: Int64;
    u1f0sp  @30: Text;
    u1f1sp  @31: Text;

    # Pack more stuff into union1 -- each should go into the same space as corresponding u1f0s*.
    u1f2s0  @32: Void;
    u1f2s1  @33: Bool;
    u1f2s8  @34: Int8;
    u1f2s16 @35: Int16;
    u1f2s32 @36: Int32;
    u1f2s64 @37: Int64;
    u1f2sp  @38: Text;
  }

  # Fill in the rest of that bitfield from earlier.
  bit2 @39: Bool;
  bit3 @40: Bool;
  bit4 @41: Bool;
  bit5 @42: Bool;
  bit6 @43: Bool;
  bit7 @44: Bool;

  # Interleave two unions to be really annoying.
  # Also declare in reverse order to make sure union discriminant values are sorted by field number
  # and not by declaration order.
  union2 @2! :union {
    u2f0s64 @54: Int64;
    u2f0s32 @52: Int32;
    u2f0s16 @50: Int16;
    u2f0s8 @47: Int8;
    u2f0s1 @45: Bool;
  }

  union3 @3! :union {
    u3f0s64 @55: Int64;
    u3f0s32 @53: Int32;
    u3f0s16 @51: Int16;
    u3f0s8 @48: Int8;
    u3f0s1 @46: Bool;
  }

  byte0 @49: UInt8;
}

struct TestUnnamedUnion {
  before @0 :Text;

  union {
    foo @1 :UInt16;
    bar @3 :UInt32;
  }

  middle @2 :UInt16;

  after @4 :Text;
}

struct TestUnionInUnion {
  # There is no reason to ever do this.
  outer :union {
    inner :union {
      foo @0 :Int32;
      bar @1 :Int32;
    }
    baz @2 :Int32;
  }
}

struct TestGroups {
  groups :union {
    foo :group {
      corge @0 :Int32;
      grault @2 :Int64;
      garply @8 :Text;
    }
    bar :group {
      corge @3 :Int32;
      grault @4 :Text;
      garply @5 :Int64;
    }
    baz :group {
      corge @1 :Int32;
      grault @6 :Text;
      garply @7 :Text;
    }
  }
}

struct TestInterleavedGroups {
  group1 :group {
    foo @0 :UInt32;
    bar @2 :UInt64;
    union {
      qux @4 :UInt16;
      corge :group {
        grault @6 :UInt64;
        garply @8 :UInt16;
        plugh @14 :Text;
        xyzzy @16 :Text;
      }

      fred @12 :Text;
    }

    waldo @10 :Text;
  }

  group2 :group {
    foo @1 :UInt32;
    bar @3 :UInt64;
    union {
      qux @5 :UInt16;
      corge :group {
        grault @7 :UInt64;
        garply @9 :UInt16;
        plugh @15 :Text;
        xyzzy @17 :Text;
      }

      fred @13 :Text;
    }

    waldo @11 :Text;
  }
}

struct TestUnionDefaults {
  s16s8s64s8Set @0 :TestUnion =
      (union0 = (u0f0s16 = 321), union1 = (u1f0s8 = 123), union2 = (u2f0s64 = 12345678901234567),
       union3 = (u3f0s8 = 55));
  s0sps1s32Set @1 :TestUnion =
      (union0 = (u0f1s0 = void), union1 = (u1f0sp = "foo"), union2 = (u2f0s1 = true),
       union3 = (u3f0s32 = 12345678));

  unnamed1 @2 :TestUnnamedUnion = (foo = 123);
  unnamed2 @3 :TestUnnamedUnion = (bar = 321, before = "foo", after = "bar");
}

struct TestNestedTypes {
  enum NestedEnum1 {
    foo @0;
    bar @1;
  }

  struct NestedStruct {
    enum NestedEnum2 {
      baz @0;
      qux @1;
      quux @2;
    }

    outerNestedEnum @0 :TestNestedTypes.NestedEnum1 = bar;
    innerNestedEnum @1 :NestedEnum2 = quux;
    listOuterNestedEnum @2 :List(NestedEnum1) = [foo, bar];
    listInnerNestedEnum @3 :List(NestedEnum2) = [quux, qux];
  }

  nestedStruct @0 :NestedStruct;

  outerNestedEnum @1 :NestedEnum1 = bar;
  innerNestedEnum @2 :NestedStruct.NestedEnum2 = quux;
}

struct TestUsing {
  using OuterNestedEnum = TestNestedTypes.NestedEnum1;
  using TestNestedTypes.NestedStruct.NestedEnum2;

  outerNestedEnum @1 :OuterNestedEnum = bar;
  innerNestedEnum @0 :NestedEnum2 = quux;
}

struct TestLists {
  # Small structs, when encoded as list, will be encoded as primitive lists rather than struct
  # lists, to save space.
  struct Struct0  { f @0 :Void; }
  struct Struct1  { f @0 :Bool; }
  struct Struct8  { f @0 :UInt8; }
  struct Struct16 { f @0 :UInt16; }
  struct Struct32 { f @0 :UInt32; }
  struct Struct64 { f @0 :UInt64; }
  struct StructP  { f @0 :Text; }

  # Versions of the above which cannot be encoded as primitive lists.
  struct Struct0c  { f @0 :Void; pad @1 :Text; }
  struct Struct1c  { f @0 :Bool; pad @1 :Text; }
  struct Struct8c  { f @0 :UInt8; pad @1 :Text; }
  struct Struct16c { f @0 :UInt16; pad @1 :Text; }
  struct Struct32c { f @0 :UInt32; pad @1 :Text; }
  struct Struct64c { f @0 :UInt64; pad @1 :Text; }
  struct StructPc  { f @0 :Text; pad @1 :UInt64; }

  list0  @0 :List(Struct0);
  list1  @1 :List(Struct1);
  list8  @2 :List(Struct8);
  list16 @3 :List(Struct16);
  list32 @4 :List(Struct32);
  list64 @5 :List(Struct64);
  listP  @6 :List(StructP);

  listlist0  @7 :List(List(Struct0));
  listlist1  @8 :List(List(Struct1));
  listlist8  @9 :List(List(Struct8));
  listlist16 @10 :List(List(Struct16));
  listlist32 @11 :List(List(Struct32));
  listlist64 @12 :List(List(Struct64));
  listlistP  @13 :List(List(StructP));

  list0c  @14 :List(Struct0c);
  list1c  @15 :List(Struct1c);
  list8c  @16 :List(Struct8c);
  list16c @17 :List(Struct16c);
  list32c @18 :List(Struct32c);
  list64c @19 :List(Struct64c);
  listPc  @20 :List(StructPc);

  listlist0c  @21 :List(List(Struct0c));
  listlist1c  @22 :List(List(Struct1c));
  listlist8c  @23 :List(List(Struct8c));
  listlist16c @24 :List(List(Struct16c));
  listlist32c @25 :List(List(Struct32c));
  listlist64c @26 :List(List(Struct64c));
  listlistPc  @27 :List(List(StructPc));

  int32ListList @28 :List(List(Int32));
  textListList @29 :List(List(Text));
  structListList @30 :List(List(TestAllTypes));
}

struct TestFieldZeroIsBit {
  bit @0 :Bool;
  secondBit @1 :Bool = true;
  thirdField @2 :UInt8 = 123;
}

struct TestListDefaults {
  lists @0 :TestLists = (
      list0  = [(f = void), (f = void)],
      list1  = [(f = true), (f = false)],
      list8  = [(f = 123), (f = 45)],
      list16 = [(f = 12345), (f = 6789)],
      list32 = [(f = 123456789), (f = 234567890)],
      list64 = [(f = 1234567890123456), (f = 2345678901234567)],
      listP  = [(f = "foo"), (f = "bar")],

      listlist0  = [[(f = void), (f = void)],[(f = void), (f = void)]],
      listlist1  = [[(f = true), (f = false)],[(f = true), (f = true)]],
      listlist8  = [[(f = 123), (f = 45)],[(f = 123), (f = 45)]],
      listlist16 = [[(f = 12345), (f = 6789)],[(f = 12345), (f = 6789)]],
      listlist32 = [[(f = 123456789), (f = 234567890)],[(f = 123456789), (f = 234567890)]],
      listlist64 = [[(f = 1234567890123456), (f = 2345678901234567)],[(f = 1234567890123456), (f = 2345678901234567)]],
      listlistP  = [[(f = "foo"), (f = "bar")],[(f = "foo"), (f = "bar")]],

      list0c  = [(f = void, pad = "foo"), (f = void, pad = "bar")],
      list1c  = [(f = true, pad = "foo"), (f = false, pad = "bar")],
      list8c  = [(f = 123, pad = "foo"), (f = 45, pad = "bar")],
      list16c = [(f = 12345, pad = "foo"), (f = 6789, pad = "bar")],
      list32c = [(f = 123456789, pad = "foo"), (f = 234567890, pad = "bar")],
      list64c = [(f = 1234567890123456, pad = "foo"), (f = 2345678901234567, pad = "bar")],
      listPc  = [(f = "foo", pad = 1234567890123456), (f = "bar", pad = 2345678901234567)],

      listlist0c  = [[(f = void, pad = "foo"), (f = void, pad = "bar")],[(f = void, pad = "foo"), (f = void, pad = "bar")]],
      listlist1c  = [[(f = true, pad = "foo"), (f = false, pad = "bar")],[(f = true, pad = "foo"), (f = false, pad = "bar")]],
      listlist8c  = [[(f = 123, pad = "foo"), (f = 45, pad = "bar")],[(f = 123, pad = "foo"), (f = 45, pad = "bar")]],
      listlist16c = [[(f = 12345, pad = "foo"), (f = 6789, pad = "bar")],[(f = 12345, pad = "foo"), (f = 6789, pad = "bar")]],
      listlist32c = [[(f = 123456789, pad = "foo"), (f = 234567890, pad = "bar")],[(f = 123456789, pad = "foo"), (f = 234567890, pad = "bar")]],
      listlist64c = [[(f = 1234567890123456, pad = "foo"), (f = 2345678901234567, pad = "bar")],[(f = 1234567890123456, pad = "foo"), (f = 2345678901234567, pad = "bar")]],
      listlistPc  = [[(f = "foo", pad = 1234567890123456), (f = "bar", pad = 2345678901234567)],[(f = "foo", pad = 1234567890123456), (f = "bar", pad = 2345678901234567)]],

      int32ListList = [[1, 2, 3], [4, 5], [12341234]],
      textListList = [["foo", "bar"], ["baz"], ["qux", "corge"]],
      structListList = [[(int32Field = 123), (int32Field = 456)], [(int32Field = 789)]]);
}

struct TestLateUnion {
  # Test what happens if the unions are not the first ordinals in the struct.  At one point this
  # was broken for the dynamic API.

  foo @0 :Int32;
  bar @1 :Text;
  baz @2 :Int16;

  theUnion @3! :union {
    qux @4 :Text;
    corge @5 :List(Int32);
    grault @6 :Float32;
  }

  anotherUnion @7! :union {
    qux @8 :Text;
    corge @9 :List(Int32);
    grault @10 :Float32;
  }
}

struct TestOldVersion {
  # A subset of TestNewVersion.
  old1 @0 :Int64;
  old2 @1 :Text;
  old3 @2 :TestOldVersion;
}

struct TestNewVersion {
  # A superset of TestOldVersion.
  old1 @0 :Int64;
  old2 @1 :Text;
  old3 @2 :TestNewVersion;
  new1 @3 :Int64 = 987;
  new2 @4 :Text = "baz";
}

struct TestStructUnion {
  un @0! :union {
    struct @1 :SomeStruct;
    object @2 :TestAnyPointer;
  }

  struct SomeStruct {
    someText @0 :Text;
    moreText @1 :Text;
  }
}

struct TestPrintInlineStructs {
  someText @0 :Text;

  structList @1 :List(InlineStruct);
  struct InlineStruct {
    int32Field @0 :Int32;
    textField @1 :Text;
  }
}

struct TestWholeFloatDefault {
  # At one point, these failed to compile in C++ because it would produce literals like "123f",
  # which is not valid; it needs to be "123.0f".
  field @0 :Float32 = 123;
  bigField @1 :Float32 = 2e30;
  const constant :Float32 = 456;
  const bigConstant :Float32 = 4e30;
}

struct TestEmptyStruct {}

struct TestConstants {
  const voidConst      :Void    = void;
  const boolConst      :Bool    = true;
  const int8Const      :Int8    = -123;
  const int16Const     :Int16   = -12345;
  const int32Const     :Int32   = -12345678;
  const int64Const     :Int64   = -123456789012345;
  const uint8Const     :UInt8   = 234;
  const uint16Const    :UInt16  = 45678;
  const uint32Const    :UInt32  = 3456789012;
  const uint64Const    :UInt64  = 12345678901234567890;
  const float32Const   :Float32 = 1234.5;
  const float64Const   :Float64 = -123e45;
  const textConst      :Text    = "foo";
  const dataConst      :Data    = "bar";
  const structConst    :TestAllTypes = (
      voidField      = void,
      boolField      = true,
      int8Field      = -12,
      int16Field     = 3456,
      int32Field     = -78901234,
      int64Field     = 56789012345678,
      uInt8Field     = 90,
      uInt16Field    = 1234,
      uInt32Field    = 56789012,
      uInt64Field    = 345678901234567890,
      float32Field   = -1.25e-10,
      float64Field   = 345,
      textField      = "baz",
      dataField      = "qux",
      structField    = (
          textField = "nested",
          structField = (textField = "really nested")),
      enumField      = baz,
      # interfaceField can't have a default

      voidList      = [void, void, void],
      boolList      = [false, true, false, true, true],
      int8List      = [12, -34, -0x80, 0x7f],
      int16List     = [1234, -5678, -0x8000, 0x7fff],
      int32List     = [12345678, -90123456, -0x80000000, 0x7fffffff],
      int64List     = [123456789012345, -678901234567890, -0x8000000000000000, 0x7fffffffffffffff],
      uInt8List     = [12, 34, 0, 0xff],
      uInt16List    = [1234, 5678, 0, 0xffff],
      uInt32List    = [12345678, 90123456, 0, 0xffffffff],
      uInt64List    = [123456789012345, 678901234567890, 0, 0xffffffffffffffff],
      float32List   = [0, 1234567, 1e37, -1e37, 1e-37, -1e-37],
      float64List   = [0, 123456789012345, 1e306, -1e306, 1e-306, -1e-306],
      textList      = ["quux", "corge", "grault"],
      dataList      = ["garply", "waldo", "fred"],
      structList    = [
          (textField = "x structlist 1"),
          (textField = "x structlist 2"),
          (textField = "x structlist 3")],
      enumList      = [qux, bar, grault]
      # interfaceList can't have a default
      );
  const enumConst      :TestEnum = corge;

  const voidListConst      :List(Void)    = [void, void, void, void, void, void];
  const boolListConst      :List(Bool)    = [true, false, false, true];
  const int8ListConst      :List(Int8)    = [111, -111];
  const int16ListConst     :List(Int16)   = [11111, -11111];
  const int32ListConst     :List(Int32)   = [111111111, -111111111];
  const int64ListConst     :List(Int64)   = [1111111111111111111, -1111111111111111111];
  const uint8ListConst     :List(UInt8)   = [111, 222] ;
  const uint16ListConst    :List(UInt16)  = [33333, 44444];
  const uint32ListConst    :List(UInt32)  = [3333333333];
  const uint64ListConst    :List(UInt64)  = [11111111111111111111];
  const float32ListConst   :List(Float32) = [5555.5, inf, -inf, nan];
  const float64ListConst   :List(Float64) = [7777.75, inf, -inf, nan];
  const textListConst      :List(Text)    = ["plugh", "xyzzy", "thud"];
  const dataListConst      :List(Data)    = ["oops", "exhausted", "rfc3092"];
  const structListConst    :List(TestAllTypes) = [
      (textField = "structlist 1"),
      (textField = "structlist 2"),
      (textField = "structlist 3")];
  const enumListConst      :List(TestEnum) = [foo, garply];
}

const globalInt :UInt32 = 12345;
const globalText :Text = "foobar";
const globalStruct :TestAllTypes = (int32Field = 54321);
const globalPrintableStruct :TestPrintInlineStructs = (someText = "foo");
const derivedConstant :TestAllTypes = (
    uInt32Field = .globalInt,
    textField = TestConstants.textConst,
    structField = TestConstants.structConst,
    int16List = TestConstants.int16ListConst,
    structList = TestConstants.structListConst);

struct TestSturdyRef {
  hostId @0 :TestSturdyRefHostId;
  objectId @1 :AnyPointer;
}

struct TestSturdyRefHostId {
  host @0 :Text;
}

struct TestSturdyRefObjectId {
  tag @0 :Tag;
  enum Tag {
    testInterface @0;
    testExtends @1;
    testPipeline @2;
    testTailCallee @3;
    testTailCaller @4;
    testMoreStuff @5;
  }
}

struct TestProvisionId {}
struct TestRecipientId {}
struct TestThirdPartyCapId {}
struct TestJoinResult {}

struct TestNameAnnotation $Cxx.name("RenamedStruct") {
  union {
    badFieldName @0 :Bool $Cxx.name("goodFieldName");
    bar @1 :Int8;
  }

  enum BadlyNamedEnum $Cxx.name("RenamedEnum") {
    foo @0;
    bar @1;
    baz @2 $Cxx.name("qux");
  }

  anotherBadFieldName @2 :BadlyNamedEnum $Cxx.name("anotherGoodFieldName");

  struct NestedStruct $Cxx.name("RenamedNestedStruct") {
    badNestedFieldName @0 :Bool $Cxx.name("goodNestedFieldName");
    anotherBadNestedFieldName @1 :NestedStruct $Cxx.name("anotherGoodNestedFieldName");

    enum DeeplyNestedEnum $Cxx.name("RenamedDeeplyNestedEnum") {
      quux @0;
      corge @1;
      grault @2 $Cxx.name("garply");
    }
  }

  badlyNamedUnion :union $Cxx.name("renamedUnion") {
    badlyNamedGroup :group $Cxx.name("renamedGroup") {
      foo @3 :Void;
      bar @4 :Void;
    }
    baz @5 :NestedStruct $Cxx.name("qux");
  }
}
