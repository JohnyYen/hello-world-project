import { gamesApi } from "@/api/client";
import type {
  GameResponse,
  GameCreate,
  GameUpdate,
  LevelResponse,
  LevelCreate,
  LevelUpdate,
  GameInstanceCreate,
  GameInstanceEnd,
  SegmentLevelCreate,
  SegmentLevelUpdate,
} from "@/api/types";

// Games
export async function getGames(token: string) {
  return gamesApi.getGames(token);
}

export async function getGame(gameId: string, token: string) {
  return gamesApi.getGame(gameId, token);
}

export async function createGame(gameCreate: GameCreate, token: string) {
  return gamesApi.createGame(gameCreate, token);
}

export async function updateGame(gameId: string, gameUpdate: GameUpdate, token: string) {
  return gamesApi.updateGame(gameId, gameUpdate, token);
}

export async function deleteGame(gameId: string, token: string) {
  return gamesApi.deleteGame(gameId, token);
}

// Levels
export async function getLevels(token: string) {
  return gamesApi.getLevels(token);
}

export async function getLevel(levelId: string, token: string) {
  return gamesApi.getLevel(levelId, token);
}

export async function createLevel(levelCreate: LevelCreate, token: string) {
  return gamesApi.createLevel(levelCreate, token);
}

export async function updateLevel(levelId: string, levelUpdate: LevelUpdate, token: string) {
  return gamesApi.updateLevel(levelId, levelUpdate, token);
}

export async function deleteLevel(levelId: string, token: string) {
  return gamesApi.deleteLevel(levelId, token);
}

// Game Instances
export async function getGameInstances(token: string) {
  return gamesApi.getGameInstances(token);
}

export async function createGameInstance(body: GameInstanceCreate, token: string) {
  return gamesApi.createGameInstance(body, token);
}

export async function endGameInstance(instanceId: string, endData: GameInstanceEnd, token: string) {
  return gamesApi.endGameInstance(instanceId, endData, token);
}

// Segment Levels
export async function getSegmentLevels(token: string) {
  return gamesApi.getSegmentLevels(token);
}

export async function createSegmentLevel(body: SegmentLevelCreate, token: string) {
  return gamesApi.createSegmentLevel(body, token);
}

export async function updateSegmentLevel(segmentLevelId: string, body: SegmentLevelUpdate, token: string) {
  return gamesApi.updateSegmentLevel(segmentLevelId, body, token);
}

export async function deleteSegmentLevel(segmentLevelId: string, token: string) {
  return gamesApi.deleteSegmentLevel(segmentLevelId, token);
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
  getGameInstances,
  createGameInstance,
  endGameInstance,
  getSegmentLevels,
  createSegmentLevel,
  updateSegmentLevel,
  deleteSegmentLevel,
};
