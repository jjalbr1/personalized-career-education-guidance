'use strict'

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { ZipkinExporter } = require('@opentelemetry/exporter-zipkin');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-base');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// Configure the Zipkin exporter
const zipkinExporter = new ZipkinExporter({
    url: 'http://localhost:9411/api/v2/spans'
});

// Configure the SDK to export telemetry data to the Zipkin instance
const sdk = new NodeSDK({
    resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'my-service'
    }),
    traceExporter: zipkinExporter,
    instrumentations: [getNodeAutoInstrumentations()]
});

// Additionally, you can configure another SDK instance to export to console if needed
// This part is optional if you only want to export to Zipkin
const consoleExporter = new ConsoleSpanExporter();
const sdkConsole = new NodeSDK({
    resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'my-service'
    }),
    traceExporter: consoleExporter,
    instrumentations: [getNodeAutoInstrumentations()]
});

// Start both SDK instances
sdk.start();
sdkConsole.start();

// Gracefully shut down the SDK on process exit
process.on('SIGTERM', () => {
    sdk.shutdown().then(() => {
        console.log('Zipkin Tracing terminated');
    }).catch((error) => {
        console.error('Error terminating Zipkin tracing', error);
    }).finally(() => {
        process.exit(0);
    });

    sdkConsole.shutdown().then(() => {
        console.log('Console Tracing terminated');
    }).catch((error) => {
        console.error('Error terminating Console tracing', error);
    });
});
