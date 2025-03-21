//
// Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
//
package io.deephaven.javascript.proto.dhinternal.jspb.map;

import jsinterop.annotations.JsPackage;
import jsinterop.annotations.JsType;

@JsType(isNative = true, name = "dhinternal.jspb.Map.Iterator", namespace = JsPackage.GLOBAL)
public interface Iterator<T> {
    IteratorResult<T> next();
}
