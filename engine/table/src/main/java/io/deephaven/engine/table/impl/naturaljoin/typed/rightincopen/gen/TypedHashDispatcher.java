//
// Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
//
// ****** AUTO-GENERATED CLASS - DO NOT EDIT MANUALLY
// ****** Run ReplicateTypedHashers or ./gradlew replicateTypedHashers to regenerate
//
// @formatter:off
package io.deephaven.engine.table.impl.naturaljoin.typed.rightincopen.gen;

import io.deephaven.api.NaturalJoinType;
import io.deephaven.chunk.ChunkType;
import io.deephaven.engine.table.ColumnSource;
import io.deephaven.engine.table.impl.naturaljoin.RightIncrementalNaturalJoinStateManagerTypedBase;
import java.util.Arrays;

/**
 * The TypedHashDispatcher returns a pre-generated and precompiled hasher instance suitable for the provided column sources, or null if there is not a precompiled hasher suitable for the specified sources.
 */
public class TypedHashDispatcher {
    private TypedHashDispatcher() {
        // static use only
    }

    public static RightIncrementalNaturalJoinStateManagerTypedBase dispatch(
            ColumnSource[] tableKeySources, ColumnSource[] originalTableKeySources, int tableSize,
            double maximumLoadFactor, double targetLoadFactor, NaturalJoinType joinType,
            boolean addOnly) {
        final ChunkType[] chunkTypes = Arrays.stream(tableKeySources).map(ColumnSource::getChunkType).toArray(ChunkType[]::new);;
        if (chunkTypes.length == 1) {
            return dispatchSingle(chunkTypes[0], tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
        }
        return null;
    }

    private static RightIncrementalNaturalJoinStateManagerTypedBase dispatchSingle(
            ChunkType chunkType, ColumnSource[] tableKeySources,
            ColumnSource[] originalTableKeySources, int tableSize, double maximumLoadFactor,
            double targetLoadFactor, NaturalJoinType joinType, boolean addOnly) {
        switch (chunkType) {
            default: throw new UnsupportedOperationException("Invalid chunk type for typed hashers: " + chunkType);
            case Char: return new RightIncrementalNaturalJoinHasherChar(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Byte: return new RightIncrementalNaturalJoinHasherByte(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Short: return new RightIncrementalNaturalJoinHasherShort(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Int: return new RightIncrementalNaturalJoinHasherInt(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Long: return new RightIncrementalNaturalJoinHasherLong(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Float: return new RightIncrementalNaturalJoinHasherFloat(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Double: return new RightIncrementalNaturalJoinHasherDouble(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
            case Object: return new RightIncrementalNaturalJoinHasherObject(tableKeySources, originalTableKeySources, tableSize, maximumLoadFactor, targetLoadFactor, joinType, addOnly);
        }
    }
}
