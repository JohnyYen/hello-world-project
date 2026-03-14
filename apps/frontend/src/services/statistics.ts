import { cookies } from "next/headers";
import {
  Configuration,
  StatisticsApi,
  XAPIStatementListResponse,
  XAPIStatementResponse,
  XAPIStatementBatchCreate,
  FeedbackCreate,
  FeedbackSchema,
} from "@workspace/api-client-ts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");
  return token?.value || "";
}

function createStatisticsApiConfiguration(): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: async () => {
      const token = await getAuthToken();
      return token;
    },
  });
}

function getStatisticsApi(): StatisticsApi {
  return new StatisticsApi(createStatisticsApiConfiguration());
}

interface GetStatementsParams {
  skip?: number;
  limit?: number;
  studentId?: number;
  verbId?: string;
  gameId?: number;
  levelId?: number;
}

async function getStatements(params: GetStatementsParams = {}): Promise<XAPIStatementListResponse> {
  const api = getStatisticsApi();
  const response = await api.getStatementsApiV1StatisticXapiStatementsGet({
    skip: params.skip,
    limit: params.limit,
    studentId: params.studentId,
    verbId: params.verbId,
    gameId: params.gameId,
    levelId: params.levelId,
  });
  return response;
}

async function getStatement(statementId: string): Promise<XAPIStatementResponse> {
  const api = getStatisticsApi();
  const response = await api.getStatementApiV1StatisticXapiStatementsStatementIdGet({ statementId });
  return response;
}

async function sendStatements(batch: XAPIStatementBatchCreate): Promise<Array<XAPIStatementResponse>> {
  const api = getStatisticsApi();
  const response = await api.sendStatementsApiV1StatisticXapiStatementsPost({ xAPIStatementBatchCreate: batch });
  return response;
}

async function submitFeedback(feedback: FeedbackCreate): Promise<FeedbackSchema> {
  const api = getStatisticsApi();
  const response = await api.submitFeedbackApiV1StatisticFeedbackPost({ feedbackCreate: feedback });
  return response;
}

interface GetStudentFeedbackHistoryParams {
  skip?: number;
  limit?: number;
}

async function getStudentFeedbackHistory(studentId: number, params: GetStudentFeedbackHistoryParams = {}): Promise<Array<FeedbackSchema>> {
  const api = getStatisticsApi();
  const response = await api.getStudentFeedbackHistoryApiV1StatisticFeedbackStudentIdGet({
    studentId,
    skip: params.skip,
    limit: params.limit,
  });
  return response;
}

export const statisticsService = {
  getStatements,
  getStatement,
  sendStatements,
  submitFeedback,
  getStudentFeedbackHistory,
};

export type {
  GetStatementsParams,
  GetStudentFeedbackHistoryParams,
};
