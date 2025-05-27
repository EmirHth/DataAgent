// MCP Server Configuration
export const mcpConfig = {
  serverName: 'data-analysis-agent',
  serverVersion: '1.0.0',
  server: {
    command: 'python',
    args: ['../DataAnalysisAgent/server.py'],
    protocol: 'stdio',
  },
  tools: [
    'load_data',
    'analyze_data', 
    'get_data_info',
    'filter_data',
    'calculate_statistics',
    'group_analysis'
  ],
  resources: [
    'current-dataset',
    'data-summary'
  ]
};

export const getMcpServerCommand = () => {
  return {
    command: mcpConfig.server.command,
    args: mcpConfig.server.args
  };
}; 