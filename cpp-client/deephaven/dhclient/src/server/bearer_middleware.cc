/*
 * Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
 */
#include "deephaven/client/server/bearer_middleware.h"
#include "deephaven/client/utility/logging.h"
#include <cstring>

using deephaven::client::kAuthorizationHeader;
using deephaven::client::kBearerPrefix;
using deephaven::client::kEnvoyPrefixHeader;

namespace deephaven::client::server {

// BearerMiddleware implementation

BearerMiddleware::BearerMiddleware(std::string* session_token, const ExtraHeaders* extra_headers, std::mutex* mutex)
    : session_token_(session_token), extra_headers_(extra_headers), mutex_(mutex) {}

void BearerMiddleware::SendingHeaders(arrow::flight::AddCallHeaders* outgoing_headers) {
  std::unique_lock<std::mutex> lock(*mutex_);
  gpr_log(GPR_DEBUG, "BearerMiddleware::SendingHeaders called");

  // Add authorization header
  if (!session_token_->empty()) {
    // session_token_ already contains the full authorization value (e.g., "Bearer abc123")
    // Don't add the prefix again!
    outgoing_headers->AddHeader(std::string(kAuthorizationHeader), *session_token_);
    gpr_log(GPR_DEBUG, "BearerMiddleware: Added authorization header, value length: %zu", session_token_->size());
  } else {
    gpr_log(GPR_ERROR, "BearerMiddleware: Session token is EMPTY! Cannot add authorization header");
  }

  // Add envoy-prefix header if present in extra headers
  for (const auto& header : *extra_headers_) {
    if (header.first == kEnvoyPrefixHeader) {
      outgoing_headers->AddHeader(std::string(kEnvoyPrefixHeader), header.second);
      gpr_log(GPR_DEBUG, "BearerMiddleware: Added envoy-prefix header, value: %s", header.second.c_str());
      break;  // Only one envoy-prefix expected
    }
  }
}

void BearerMiddleware::ReceivedHeaders(const arrow::flight::CallHeaders& incoming_headers) {
  // Look for authorization header in incoming headers
  auto auth_headers = incoming_headers.find(std::string(kAuthorizationHeader));

  if (auth_headers == incoming_headers.end()) {
    return;
  }

  // Convert the header value to string
  // Arrow Flight may return string_view, so we explicitly convert
  std::string auth_value = std::string(auth_headers->second);

  // Check if this value starts with "Bearer " - only update if it's a Bearer token
  size_t prefix_len = kBearerPrefix.size();
  if (auth_value.size() > prefix_len &&
      auth_value.compare(0, prefix_len, kBearerPrefix) == 0) {
    // Store the FULL authorization value (including "Bearer " prefix)
    // This matches what SendingHeaders expects
    std::unique_lock<std::mutex> lock(*mutex_);
    *session_token_ = std::move(auth_value);
    gpr_log(GPR_DEBUG, "BearerMiddleware: Updated session token from response headers");
  }
}

void BearerMiddleware::CallCompleted(const arrow::Status& status) {
  // Nothing to do on call completion
}

// BearerMiddlewareFactory implementation

BearerMiddlewareFactory::BearerMiddlewareFactory(std::string* session_token, const ExtraHeaders* extra_headers, std::mutex* mutex)
    : session_token_(session_token), extra_headers_(extra_headers), mutex_(mutex) {}

void BearerMiddlewareFactory::StartCall(
    const arrow::flight::CallInfo& info,
    std::unique_ptr<arrow::flight::ClientMiddleware>* middleware) {
  *middleware = std::make_unique<BearerMiddleware>(session_token_, extra_headers_, mutex_);
}

}  // namespace deephaven::client::server


