/*
 * Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
 */
#pragma once

#include <cstdarg>
#include <cstdio>
#include <iostream>
#include <cstring>

namespace deephaven::client::utility {

// Log severity levels (compatible with gpr_log)
#ifndef GPR_ERROR
#define GPR_ERROR 2
#endif
#ifndef GPR_INFO
#define GPR_INFO 1
#endif
#ifndef GPR_DEBUG
#define GPR_DEBUG 0
#endif

// Define gpr_log_severity type for compatibility
typedef int gpr_log_severity;

/**
 * Logging function compatible with gpr_log.
 * Replacement for gpr_log that works even when gRPC doesn't provide it.
 *
 * @param severity The log level (GPR_ERROR, GPR_INFO, or GPR_DEBUG)
 * @param format Printf-style format string
 * @param ... Variable arguments matching the format string
 */
inline void DeephavenLog(int severity, const char* format, ...) {
  va_list args;
  va_start(args, format);

  // Determine output stream and prefix based on severity
  const char* level_str;
  std::ostream* out_stream;

  switch (severity) {
    case GPR_ERROR:
      level_str = "ERROR";
      out_stream = &std::cerr;
      break;
    case GPR_INFO:
      level_str = "INFO";
      out_stream = &std::cout;
      break;
    case GPR_DEBUG:
      level_str = "DEBUG";
      out_stream = &std::cout;
      break;
    default:
      level_str = "UNKNOWN";
      out_stream = &std::cout;
      break;
  }

  // Format the message
  char buffer[4096];
  vsnprintf(buffer, sizeof(buffer), format, args);
  va_end(args);

  // Output with severity prefix
  *out_stream << "[" << level_str << "] " << buffer << std::endl;
}

}  // namespace deephaven::client::utility

// Define gpr_log macro to use our wrapper
// This replaces the gpr_log function that may not be available in newer gRPC
#ifdef gpr_log
#undef gpr_log
#endif

#define gpr_log ::deephaven::client::utility::DeephavenLog

