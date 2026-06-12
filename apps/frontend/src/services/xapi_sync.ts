export const convertXAPIStatementToSyncEventPayload = (statement: object) => {
  // Convert a complete xAPI statement to the sync event payload format
  // Expected input format (complete xAPI statement):
  // {
  //   "id": "<uuid>",
  //   "actor": {"account": {"homePage": "hello-world-game", "name": "<user_id>"}},
  //   "verb": {"id": "<verb_iri>", "display": {"es": "<display_text>"}},
  //   "object": {"id": "<object_id>", "definition": {"type": "<activity_type>", "name": {"es": "<object_name>"}}},
  //   "result": {"success": <bool>, "completion": <bool>, "score": {"raw": <num>, "scaled": <num>}},
  //   "context": {"platform": "Hello World Game", "language": "es", "extensions": {}},
  //   "timestamp": "<iso_datetime>"
  // }

  // Expected output format (sync event payload):
  // {
  //   "statement_id": "<uuid>",
  //   "verb_id": "<verb_iri>",
  //   "verb_display": "<display_text>",
  //   "object_type": "<level|game|assessment|segment|exercise|puzzle>",
  //   "object_id": "<id_without_hello_world_prefix>",
  //   "object_name": "<object_name>",
  //   "actor_id": "<user_id>",
  //   "result": {
  //     "score_raw": <num or null>,
  //     "score_scaled": <num or null>,
  //     "success": <bool>,
  //     "completion": <bool>,
  //     "duration": "<duration_string or empty>"
  //   },
  //   "timestamp": "<iso_datetime>"
  // }

  const stmt = statement as any;

  // Helper to get activity type from xAPI object definition
  const getActivityTypeFromObject = (): string => {
    const objectType = stmt.object.definition?.type || "";
    if (objectType.includes("level")) return "level";
    if (objectType.includes("game")) return "game";
    if (objectType.includes("assessment")) return "assessment";
    if (objectType.includes("segment")) return "segment";
    if (objectType.includes("exercise")) return "exercise";
    if (objectType.includes("puzzle")) return "puzzle";
    return "activity";
  };

  // Helper to extract activity ID from xAPI object ID
  const getActivityIdFromObject = (): string => {
    const objectId = stmt.object.id || "";
    // Remove hello-world:// prefix and any path components
    const match = objectId.match(/[^:]+:\/\/(?:[^\/]+\/)?([^\/]+)$/);
    return match ? match[1] : objectId;
  };

  return {
    "statement_id": stmt.id,
    "verb_id": stmt.verb.id,
    "verb_display": stmt.verb.display?.es || stmt.verb.display?.en || "",
    "object_type": getActivityTypeFromObject(),
    "object_id": getActivityIdFromObject(),
    "object_name": stmt.object.definition?.name?.es || stmt.object.definition?.name?.en || "",
    "actor_id": stmt.actor.account?.name || "",
    "result": {
      "score_raw": stmt.result?.score?.raw || null,
      "score_scaled": stmt.result?.score?.scaled || null,
      "success": stmt.result?.success || false,
      "completion": stmt.result?.completion || false,
      "duration": stmt.result?.duration || ""
    },
    "timestamp": stmt.timestamp
  };
};

export const sendXAPIStatementToSyncEvents = async (statement: object) => {
  // Convert the complete xAPI statement to sync event payload format
  const eventPayload = convertXAPIStatementToSyncEventPayload(statement);

  // Start a sync session
  const sessionResponse = await fetch("/api/v1/sync/sync-sessions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ instance_id: gameInstanceId })
  });

  if (!sessionResponse.ok) {
    throw new Error(`Failed to start sync session: ${sessionResponse.statusText}`);
  }

  const session = await sessionResponse.json();

  // Send the sync event with converted payload
  const eventResponse = await fetch(
    `/api/v1/sync/sync-events`, 
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sync_session_id: session.session_id,
        event_type: "xapi_statement",
        payload: eventPayload,
        client_event_id: statement.id
      })
    }
  );

  if (!eventResponse.ok) {
    throw new Error(`Failed to send sync event: ${eventResponse.statusText}`);
  }

  // End the sync session
  await fetch(`/api/v1/sync/sync-sessions/${session.session_id}/end`, {
    method: "PUT"
  });

  return await eventResponse.json();
};

export const sendXAPIToDirectEndpoint = async (statement: object) => {
  const response = await fetch("/api/v1/xapi/statements", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ statements: [statement] })
  });

  if (!response.ok) {
    throw new Error(`Failed to send xAPI statement: ${response.statusText}`);
  }

  return await response.json();
};

// Helper functions
getActivityTypeFromObjectId(objectId: string): string {
  if (objectId.includes("://level/")) return "level";
  if (objectId.includes("://segment/")) return "segment";
  if (objectId.includes("://game/")) return "game";
  if (objectId.includes("://assessment/")) return "assessment";
  return "activity";
}

getActivityIdFromObjectId(objectId: string): string {
  // Extract the part after the last slash
  const match = objectId.match(/\/([^\/]+)$/);
  return match ? match[1] : objectId;
}

// Example usage:
const handleXAPIStatement = async (statement: object, config?: { useDirectEndpoint?: boolean }) => {
  try {
    const useDirectEndpoint = config?.useDirectEndpoint || false;
    
    if (useDirectEndpoint) {
      return await sendXAPIToDirectEndpoint(statement);
    } else {
      return await sendXAPIStatementToSyncEvents(statement);
    }
  } catch (error) {
    console.error("Error processing xAPI statement:", error);
    throw error;
  }
};
