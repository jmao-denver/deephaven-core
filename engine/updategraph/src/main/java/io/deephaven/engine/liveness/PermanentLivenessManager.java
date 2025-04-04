//
// Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
//
package io.deephaven.engine.liveness;

import io.deephaven.util.Utils;
import org.jetbrains.annotations.NotNull;

import java.util.stream.Stream;

/**
 * <p>
 * A {@link LivenessManager} implementation that will never release its referents.
 * <p>
 * Instances expect to be used on exactly one thread, and hence do not take any measures to ensure thread safety.
 */
public final class PermanentLivenessManager implements LivenessManager {

    PermanentLivenessManager() {}

    @Override
    public boolean tryManage(@NotNull LivenessReferent referent) {
        if (Liveness.REFERENCE_TRACKING_DISABLED) {
            return true;
        }
        if (!referent.tryRetainReference()) {
            return false;
        }
        if (Liveness.DEBUG_MODE_ENABLED) {
            Liveness.log.info().append("LivenessDebug: PermanentLivenessManager managing ")
                    .append(Utils.REFERENT_FORMATTER, referent).append(" for ").append(new LivenessDebugException())
                    .endl();
        }
        return true;
    }

    @Override
    public boolean tryUnmanage(@NotNull LivenessReferent referent) {
        throw new UnsupportedOperationException("PermanentLivenessManager cannot unmanage referents");
    }

    @Override
    public boolean tryUnmanage(@NotNull Stream<? extends LivenessReferent> referents) {
        throw new UnsupportedOperationException("PermanentLivenessManager cannot unmanage referents");
    }
}
