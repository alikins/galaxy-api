import logging

from prometheus_client import Counter
# Histogram, Gauge

log = logging.getLogger(__name__)

collection_import_attempts = Counter(
    "galaxy_api_collection_import_attempts", "count of collection import attempts"
)

collection_import_failures = Counter(
    "galaxy_api_collection_import_failures", "count of collection import failures"
)

collection_import_successes = Counter(
    "galaxy_api_collection_import_successes", "count of collections imported succesfully"
)

collection_artifact_download_attempts = Counter(
    "galaxy_api_collection_artifact_download_attempts",
    "count of collection artifact download attempts"
)

collection_artifact_download_failures = Counter(
    "galaxy_api_collection_artifact_download_failures",
    "count of collection artifact download failures",
    ["status"]
)

collection_artifact_download_successes = Counter(
    "galaxy_api_collection_artifact_download_successes",
    "count of succesful collection artifact downloads"
)

auth_by_rh_id_attempts = Counter(
    "galaxy_api_auth_by_rh_id_attempts",
    "count of attempts to auth by check x-rh-identity header"
)

auth_by_rh_id_failures = Counter(
    "galaxy_api_auth_by_rh_id_failures",
    "count of failed attempts to auth by check x-rh-identity header"
)

auth_rh_entitlement_required_perm_attempts = Counter(
    "galaxy_api_auth_rh_entitlement_required_perm_attempts",
    "count of attempts to check if a request has the required entitlements"
)

auth_rh_entitlement_required_perm_failures = Counter(
    "galaxy_api_auth_rh_entitlement_required_perm_failures",
    "count of failed attempts when checking if request has the required entitlements"
)

auth_rh_entitlement_required_perm_successes = Counter(
    "galaxy_api_auth_rh_entitlement_required_perm_successes",
    "count of successful attempts when checking if request has the required entitlements"
)
# galaxy_pulp_api_exceptions
