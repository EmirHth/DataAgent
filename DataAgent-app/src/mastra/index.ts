import { Mastra } from '@mastra/core/mastra';
import { PinoLogger } from '@mastra/loggers';
import { LibSQLStore } from '@mastra/libsql';

import { dataAnalysisAgent } from './agents/data-analysis-agent';

export const mastra = new Mastra({
  agents: { dataAnalysisAgent },
  storage: new LibSQLStore({
    // stores telemetry, evals, ... into memory storage, if it needs to persist, change to file:../mastra.db
    url: ":memory:",
  }),
  logger: new PinoLogger({
    name: 'DataAgent',
    level: 'info',
  }),
});
