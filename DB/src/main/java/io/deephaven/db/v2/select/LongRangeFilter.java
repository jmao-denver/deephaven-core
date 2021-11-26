/* ---------------------------------------------------------------------------------------------------------------------
 * AUTO-GENERATED CLASS - DO NOT EDIT MANUALLY - for any changes edit CharRangeFilter and regenerate
 * ------------------------------------------------------------------------------------------------------------------ */
package io.deephaven.db.v2.select;

import io.deephaven.db.tables.ColumnDefinition;
import io.deephaven.db.tables.TableDefinition;
import io.deephaven.db.util.DhLongComparisons;
import io.deephaven.db.v2.select.chunkfilters.LongRangeComparator;
import io.deephaven.db.v2.sources.ColumnSource;
import io.deephaven.db.v2.utils.Index;
import io.deephaven.gui.table.filters.Condition;
import io.deephaven.util.QueryConstants;
import io.deephaven.util.type.TypeUtils;

public class LongRangeFilter extends AbstractRangeFilter {
    final long upper;
    final long lower;

    public LongRangeFilter(String columnName, long val1, long val2, boolean lowerInclusive, boolean upperInclusive) {
        super(columnName, lowerInclusive, upperInclusive);

        if(DhLongComparisons.gt(val1, val2)) {
            upper = val1;
            lower = val2;
        } else {
            upper = val2;
            lower = val1;
        }
    }

    static SelectFilter makeLongRangeFilter(String columnName, Condition condition, String value) {
        switch (condition) {
            case LESS_THAN:
                return new LongRangeFilter(columnName, RangeConditionFilter.parseLongFilter(value), QueryConstants.NULL_LONG, true, false);
            case LESS_THAN_OR_EQUAL:
                return new LongRangeFilter(columnName, RangeConditionFilter.parseLongFilter(value), QueryConstants.NULL_LONG, true, true);
            case GREATER_THAN:
                return new LongRangeFilter(columnName, RangeConditionFilter.parseLongFilter(value), QueryConstants.MAX_LONG, false, true);
            case GREATER_THAN_OR_EQUAL:
                return new LongRangeFilter(columnName, RangeConditionFilter.parseLongFilter(value), QueryConstants.MAX_LONG, true, true);
            default:
                throw new IllegalArgumentException("RangeConditionFilter does not support condition " + condition);
        }
    }

    @Override
    public void init(TableDefinition tableDefinition) {
        if (chunkFilter != null) {
            return;
        }

        final ColumnDefinition<?> def = tableDefinition.getColumn(columnName);
        if (def == null) {
            throw new RuntimeException("Column \"" + columnName + "\" doesn't exist in this table, available columns: " + tableDefinition.getColumnNames());
        }

        final Class<?> colClass = TypeUtils.getUnboxedTypeIfBoxed(def.getDataType());
        if (colClass != long.class) {
            throw new RuntimeException("Column \"" + columnName + "\" expected to be long: " + colClass);
        }

        initChunkFilter();
    }

    ChunkFilter initChunkFilter() {
        return (chunkFilter = LongRangeComparator.makeLongFilter(lower, upper, lowerInclusive, upperInclusive));
    }

    @Override
    public LongRangeFilter copy() {
        return new LongRangeFilter(columnName, lower, upper, lowerInclusive, upperInclusive);
    }

    @Override
    public String toString() {
        return "LongRangeFilter(" + columnName + " in " +
                (lowerInclusive ? "[" : "(") + lower + "," + upper +
                (upperInclusive ? "]" : ")") + ")";
    }

    @Override
    Index binarySearch(Index selection, ColumnSource columnSource, boolean usePrev, boolean reverse) {
        if (selection.isEmpty()) {
            return selection;
        }

        //noinspection unchecked
        final ColumnSource<Long> longColumnSource = (ColumnSource<Long>)columnSource;

        final long startValue = reverse ? upper : lower;
        final long endValue = reverse ? lower : upper;
        final boolean startInclusive = reverse ? upperInclusive : lowerInclusive;
        final boolean endInclusive = reverse ? lowerInclusive : upperInclusive;
        final int compareSign = reverse ? - 1 : 1;

        long lowerBoundMin = bound(selection, usePrev, longColumnSource, 0, selection.size(), startValue, startInclusive, compareSign, false);
        long upperBoundMin = bound(selection, usePrev, longColumnSource, lowerBoundMin, selection.size(), endValue, endInclusive, compareSign, true);

        return selection.subindexByPos(lowerBoundMin, upperBoundMin);
    }

    private long bound(Index selection, boolean usePrev, ColumnSource<Long> longColumnSource, long minPosition, long maxPosition, long targetValue, boolean inclusive, int compareSign, boolean end) {
        while (minPosition < maxPosition) {
            final long midPos = (minPosition + maxPosition) / 2;
            final long midIdx = selection.get(midPos);

            final long compareValue = usePrev ? longColumnSource.getPrevLong(midIdx) : longColumnSource.getLong(midIdx);
            final int compareResult = compareSign * DhLongComparisons.compare(compareValue, targetValue);

            if (compareResult < 0) {
                minPosition = midPos + 1;
            } else if (compareResult > 0) {
                maxPosition = midPos;
            } else {
                if (end) {
                    if (inclusive) {
                        minPosition = midPos + 1;
                    } else {
                        maxPosition = midPos;
                    }
                } else {
                    if (inclusive) {
                        maxPosition = midPos;
                    } else {
                        minPosition = midPos + 1;
                    }
                }
            }
        }
        return minPosition;
    }
}
