/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

#include <napi.h>
#include <vector>

#include "Policy.hh"
#include "PolicyWatcher.hh"

using namespace Napi;

Value DisposeWatcher(const CallbackInfo &info)
{
  auto watcher = (PolicyWatcher *)info.Data();
  watcher->Dispose();
  return info.Env().Null();
}

Value CreateWatcher(const CallbackInfo &info)
{
  auto env = info.Env();

#if !defined(WINDOWS) && !defined(MACOS)
  throw TypeError::New(env, "Unsupported platform");
#endif

  if (info.Length() < 4)
    throw TypeError::New(env, "Expected 3 arguments");
  else if (!info[0].IsString())
    throw TypeError::New(env, "Expected first arg to be string");
  else if (!info[1].IsString())
    throw TypeError::New(env, "Expected second arg to be string");
  else if (!info[2].IsObject())
    throw TypeError::New(env, "Expected third arg to be object");
  else if (!info[3].IsFunction())
    throw TypeError::New(env, "Expected fourth arg to be function");

  auto rawPolicies = info[2].As<Object>();
  auto policies = std::vector<std::unique_ptr<Policy>>();
  auto watcher = new PolicyWatcher(info[0].As<String>(), info[1].As<String>(), info[3].As<Function>());

  for (auto const &item : rawPolicies)
  {
    auto rawPolicyName = item.first.As<String>();
    auto rawPolicyValue = static_cast<Value>(item.second);

    if (!rawPolicyValue.IsObject())
      throw TypeError::New(env, "Expected policy to be object");

    auto rawPolicy = rawPolicyValue.As<Object>();
    auto rawPolicyType = rawPolicy.Get("type");

    if (!rawPolicyType.IsString())
      throw TypeError::New(env, "Expected policy type to be string");

    auto policyType = std::string(rawPolicyType.As<String>());

    if (policyType == "string") {
      watcher->AddStringPolicy(rawPolicyName.As<String>());
    }
    else if (policyType == "number") {
      watcher->AddNumberPolicy(rawPolicyName.As<String>());
    } else if (policyType == "boolean") {
      watcher->AddBooleanPolicy(rawPolicyName.As<String>());
    } else {
      throw TypeError::New(env, "Unknown policy type '" + policyType + "'");
    }
  }

  watcher->Queue();

  auto result = Object::New(env);
  result.Set(String::New(env, "dispose"), Function::New(env, DisposeWatcher, "disposeWatcher", watcher));

  return result;
}

Object Init(Env env, Object exports)
{
  return Function::New(env, CreateWatcher, "createWatcher");
}

NODE_API_MODULE(vscodepolicy, Init)