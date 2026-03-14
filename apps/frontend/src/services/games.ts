import { cookies } from "next/headers";
import {
  Configuration,
  GamesApi,
  GameListResponse,
  SingleGameResponse,
  GameCreate,
  GameCreateResponse,
  GameUpdate,
  GameUpdateResponse,
  GameDeleteResponse,
  LevelListResponse,
  SingleLevelResponse,
  LevelCreate,
  LevelCreateResponse,
  LevelUpdate,
  LevelUpdateResponse,
  LevelDeleteResponse,
  SegmentLevelListResponse,
  SegmentLevelCreate,
  SegmentLevelCreateResponse,
  SegmentLevelUpdate,
  SegmentLevelUpdateResponse,
  SegmentLevelDeleteResponse,
  GameInstanceListResponse,
  GameInstanceCreate,
  GameInstanceCreateResponse,
  GameInstanceEnd,
  GameInstanceEndResponse,
  SingleGameInstanceResponse,
} from "@workspace/api-client-ts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");
  return token?.value || "";
}

function createGamesApiConfiguration(): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: async () => {
      const token = await getAuthToken();
      return token;
    },
  });
}

function getGamesApi(): GamesApi {
  return new GamesApi(createGamesApiConfiguration());
}

interface GetGamesParams {
  skip?: number;
  limit?: number;
}

async function getGames(params: GetGamesParams = {}): Promise<GameListResponse> {
  const api = getGamesApi();
  const response = await api.getGamesApiV1GamesGet({
    skip: params.skip,
    limit: params.limit,
  });
  return response;
}

async function getGame(gameId: number): Promise<SingleGameResponse> {
  const api = getGamesApi();
  const response = await api.getGameApiV1GamesGameIdGet({ gameId });
  return response;
}

async function createGame(gameCreate: GameCreate): Promise<GameCreateResponse> {
  const api = getGamesApi();
  const response = await api.createGameApiV1GamesPost({ gameCreate });
  return response;
}

async function updateGame(gameId: number, gameUpdate: GameUpdate): Promise<GameUpdateResponse> {
  const api = getGamesApi();
  const response = await api.updateGameApiV1GamesGameIdPut({ gameId, gameUpdate });
  return response;
}

async function deleteGame(gameId: number): Promise<GameDeleteResponse> {
  const api = getGamesApi();
  const response = await api.deleteGameApiV1GamesGameIdDelete({ gameId });
  return response;
}

interface GetLevelsParams {
  skip?: number;
  limit?: number;
}

async function getLevels(gameId: number, params: GetLevelsParams = {}): Promise<LevelListResponse> {
  const api = getGamesApi();
  const response = await api.getGameLevelsApiV1GamesGameIdLevelsGet({
    gameId,
    skip: params.skip,
    limit: params.limit,
  });
  return response;
}

async function getLevel(levelId: number): Promise<SingleLevelResponse> {
  const api = getGamesApi();
  const response = await api.getLevelApiV1LevelsLevelIdGet({ levelId });
  return response;
}

async function createLevel(gameId: number, levelCreate: LevelCreate): Promise<LevelCreateResponse> {
  const api = getGamesApi();
  const response = await api.createGameLevelApiV1GamesGameIdLevelsPost({ gameId, levelCreate });
  return response;
}

async function updateLevel(levelId: number, levelUpdate: LevelUpdate): Promise<LevelUpdateResponse> {
  const api = getGamesApi();
  const response = await api.updateLevelApiV1LevelsLevelIdPut({ levelId, levelUpdate });
  return response;
}

async function deleteLevel(levelId: number): Promise<LevelDeleteResponse> {
  const api = getGamesApi();
  const response = await api.deleteLevelApiV1LevelsLevelIdDelete({ levelId });
  return response;
}

interface GetSegmentsParams {
  skip?: number;
  limit?: number;
}

async function getSegments(levelId: number, params: GetSegmentsParams = {}): Promise<SegmentLevelListResponse> {
  const api = getGamesApi();
  const response = await api.getLevelSegmentsApiV1SegmentsLevelIdSegmentsGet({
    levelId,
    skip: params.skip,
    limit: params.limit,
  });
  return response;
}

async function createSegment(levelId: number, segmentCreate: SegmentLevelCreate): Promise<SegmentLevelCreateResponse> {
  const api = getGamesApi();
  const response = await api.createLevelSegmentApiV1SegmentsLevelIdSegmentsPost({ levelId, segmentLevelCreate: segmentCreate });
  return response;
}

async function updateSegment(segmentId: number, segmentUpdate: SegmentLevelUpdate): Promise<SegmentLevelUpdateResponse> {
  const api = getGamesApi();
  const response = await api.updateSegmentApiV1SegmentsSegmentIdPut({ segmentId, segmentLevelUpdate: segmentUpdate });
  return response;
}

async function deleteSegment(segmentId: number): Promise<SegmentLevelDeleteResponse> {
  const api = getGamesApi();
  const response = await api.deleteSegmentApiV1SegmentsSegmentIdDelete({ segmentId });
  return response;
}

interface GetGameInstancesParams {
  skip?: number;
  limit?: number;
  statusFilter?: string;
}

async function getGameInstances(gameId: number, params: GetGameInstancesParams = {}): Promise<GameInstanceListResponse> {
  const api = getGamesApi();
  const response = await api.listGameInstancesApiV1GameInstancesGameIdInstancesGet({
    gameId,
    skip: params.skip,
    limit: params.limit,
    statusFilter: params.statusFilter,
  });
  return response;
}

async function getGameInstance(instanceId: number): Promise<SingleGameInstanceResponse> {
  const api = getGamesApi();
  const response = await api.getInstanceApiV1GameInstancesInstanceIdGet({ instanceId });
  return response;
}

async function startGameInstance(gameId: number, instanceCreate: GameInstanceCreate): Promise<GameInstanceCreateResponse> {
  const api = getGamesApi();
  const response = await api.createGameInstanceApiV1GameInstancesGameIdInstancesPost({ gameId, gameInstanceCreate: instanceCreate });
  return response;
}

async function endGameInstance(instanceId: number, endData?: GameInstanceEnd): Promise<GameInstanceEndResponse> {
  const api = getGamesApi();
  const response = await api.endInstanceApiV1GameInstancesInstanceIdEndPut({ instanceId, gameInstanceEnd: endData });
  return response;
}

export const gamesService = {
  getGames,
  getGame,
  createGame,
  updateGame,
  deleteGame,
  getLevels,
  getLevel,
  createLevel,
  updateLevel,
  deleteLevel,
  getSegments,
  createSegment,
  updateSegment,
  deleteSegment,
  getGameInstances,
  getGameInstance,
  startGameInstance,
  endGameInstance,
};

export type {
  GetGamesParams,
  GetLevelsParams,
  GetSegmentsParams,
  GetGameInstancesParams,
};
