/*
 * Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
 */
#pragma once

#include <memory>
#include <mutex>
#include <string>
#include <arrow/flight/client_middleware.h>

namespace deephaven::client::server {

/**
 * Middleware for managing Bearer token authentication in Arrow Flight calls.
 * This middleware:
 * - Adds the Bearer token to outgoing request headers
 * - Extracts updated Bearer tokens from incoming response headers
 * - Uses Server's sessionToken_ and mutex_ for thread-safe access
 */
class BearerMiddleware : public arrow::flight::ClientMiddleware {
public:
  /**
   * Construct a BearerMiddleware with references to Server's session token and mutex.
   * @param session_token Pointer to Server's session token (must outlive this middleware)
   * @param mutex Pointer to Server's mutex (must outlive this middleware)
   */
  BearerMiddleware(std::string* session_token, std::mutex* mutex);

  /**
   * Called before sending headers. Adds the Bearer token to the authorization header.
   */
  void SendingHeaders(arrow::flight::AddCallHeaders* outgoing_headers) override;

  /**
   * Called when headers are received. Extracts and updates the Bearer token if present.
   * Note: Arrow Flight CallHeaders maps header names to single string values.
   */
  void ReceivedHeaders(const arrow::flight::CallHeaders& incoming_headers) override;

  /**
   * Called when the call is completed.
   */
  void CallCompleted(const arrow::Status& status) override;

private:
  std::string* session_token_;  // Points to Server::sessionToken_
  std::mutex* mutex_;            // Points to Server::mutex_

  static constexpr const char* kAuthorizationKey = "authorization";
  static constexpr const char* kBearerPrefix = "Bearer ";
};

/**
 * Factory for creating BearerMiddleware instances.
 * The factory holds raw pointers to Server's session token and mutex,
 * which is safe because Server owns the FlightClient which uses this factory.
 */
class BearerMiddlewareFactory : public arrow::flight::ClientMiddlewareFactory {
public:
  /**
   * Construct a factory with references to Server's session token and mutex.
   * @param session_token Pointer to Server's session token (must outlive this factory)
   * @param mutex Pointer to Server's mutex (must outlive this factory)
   */
  BearerMiddlewareFactory(std::string* session_token, std::mutex* mutex);

  /**
   * Called when a new call starts. Creates a BearerMiddleware instance.
   */
  void StartCall(const arrow::flight::CallInfo& info,
                 std::unique_ptr<arrow::flight::ClientMiddleware>* middleware) override;

private:
  std::string* session_token_;  // Points to Server::sessionToken_
  std::mutex* mutex_;            // Points to Server::mutex_
};

}  // namespace deephaven::client::server


