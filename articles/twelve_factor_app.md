# The twelve-factor app

Personal notes based on the twelve-factor app methodology.
See the original site, Written by Adam Wiggins: https://12factor.net

## Introduction

- Methodology for building SaaS apps.
- Automation to reduce friction for new contributors.
- Offer maximum portability between environments.
- Minimize divergence between development and production.
- Scale up without significant changes.

## 1. Codebase

- Use a version control system (Git, Mercurial, Subversion)
- Codebase is a single or set of code repositories.
- Multiple codebases: distributed system $\ne$ app.
  - Each codebase can comply with 12FA.
- Multiple apps sharing code is not allowed.
  - Factor shared code into libraries.
  - Include libraries via dependency manager.
- An app will have many deploys
  - Deploy: Running instance of the app.
  - Normally production, staging and development in local environments.
  - Codebase is the same for all deploys.
  - Different versions may be active in each deployment.

## 2. Dependencies

- Packing system for distributing support libraries.
- Libraries can be system-wide (site packages) or scoped into the directory (vendoring/bundling).
- The 12FA must declare dependencies via a dependency declaration manifest.
  - E.g Pip for Python
- Must use a dependency isolation tool to avoid leaked in dependencies.
  - E.g Virtualenv for Python.
- Dependency specification is applied uniformly to both production and development.
- This simplifies setup for new developers.
- 12FA app must also vendor system tools that could not be installed on the system (e.g curl).

## 3. Config

- Config is everything that may vary between deploys.
  - Credentials to external service, a host name for a deploy, database handles.
- Configuration must be separate from code.
  - Code should not substantially vary across deploys.
  - Ask yourself: Can the codebase be made open source without compromising credentials/secrets?
- Configs that don't vary between deploys can be done in code.
- For configs that do vary, can be done in code but not checked into revision control.
- A better alternative is to store using environment variables.
  - Hard to check into a repo.
  - Language and OS agnostic.
- Don't group env vars by deploys (development, test, production, etc.)
  - Won't scale well, hard to track.
  - Declare env vars as granular controls.

## 4. Backing services

- Backing service is any service the app consumers over the network.
  - Databases, messaging queues, email service or caching systems.
- Can be locally managed services or third-party services.
- The 12FA must not make any distinction between local or third-party services.
  - Both are attached resources accessed via URL or credentials on config.
  - Should be able to swap locally managed service for third-party service without code changes (e.g local MySQL for RDS).
- Each service is a resource.
- The app should treat resources as attached, indicating loose coupling.
- The app should be able to handle resources being attached and detached from deploys without code changes.
  - E.g Database goes down, a new instance is attached via env config change.

## 5. Build, release and run

- For a codebase to become a deploy it must:
  - Be built: Convert a version of the code (specific commit) of the repo into an executable (binaries and assets).
  - Release: Combination of build and config - ready for execution in an execution environment. 
  - Run(time): Runs the app in the execution environment by launching some set of processes for the app.
- None of these changes can be done at runtime for a 12FA.
- Deployment tools offer release management tools which provide the ability to roll back to a previous release.
- Every release has a unique ID (timestamp or incrementing version number).
- Releases are append only. Changes require the creation of a new release.
- Builds are initiated by the app developer when new code is deployed.
- The run stage should be simple to avoid complex problems when developers aren't available to fix.
- The build stage can be more complex since there is always a developer driving a deploy.

## 6. Processes

- The app is executed as one or more processes in the execution environment
- Processes should be stateless and share nothing.
- Any data that needs to be persisted should use a backing service.
- Memory/file system can be used a cache to store temporary data.
  - Never assume that data from a previous request will be available.
- Session state data can be stored in Memcached or Redis (datastores with time-expiration).

## 7. Port Binding

- Web apps should export HTTP as a service by binding to a port and listening to requests coming in to that port.
- Development visit a local host port for development.
- In deployment, a routing layer handles routing requests from public hostname to port bound web processes.
- This means that one app can become a backing service for another app.

## 8. Concurrency

- Processes follow unix process model for running service daemons.
- App can handle diverse workloads based on process type.
  - Web process for HTTP requests
  - Worker process for long tasks
- Individual processes can multiplex via threads or async/event models.
- Application can scale horizontally due to the the characteristics we've added to the 12FA.
- Process formation: Collection of process types and number of processes.
- 12FA should rely on OS process manager to manage output streams, respond to crashes and handle user restarts.

## 9. Disposability

- Disposable processes: Can be started/stopped at any moment.
- This requires short startup times.
  - Consequence: Agility for releases, easy to scale up.
- Processes must be able to shut down gracefully when they receive a SIGTERM.
  - Stops receiving new requests, finishes on going requests, exit.
- For long running jobs (workers) - return the job to the processing queue.
- Processes should be robust against sudden deaths due to hardware failure.

## 10. Dev/prod parity

- Gaps between development and production appear as
  - Time gap: Time changes take to go into production.
  - Personnel gap: Different people write and deploy code.
  - Tools gap: Stacks are first changed in development, so they may be different to production.
- 12FA should be design for continuous deployment.
- Gap between dev/prod should be small. 
  - Small time gap: Code should be deployed minutes/hours after its written.
  - Small personnel gap: Developers should be involved in deployment.
  - Small tools gap: Tool sets should be a similar as possible.
- Libraries can be used to guarantee parity for backing services by proving multiple adapters.
  - These libraries also help with porting new backing services.
- The same backing services should be used for development and production.

## 11. Logs

- Logs are the stream of aggregated, time ordered events collected from all ouput streams of running and backing services together.
- Logs have no fixed beginning or end.
- 12FA shouldn't worry about routing/storing output streams.
  - Should write to stdout.
  - Local devs will view this in the terminal.
  - Process stream will be captured by execution environment and unified in one or more destination for viewing and archiving.
  - Streams can be stored in log indexing systems or data warehouses for advanced analysis.
  
## 12. Admin processes

- Process formation are regular processes for app business needs.
- Developers also perform administrative or maintenance tasks such as database migrations or running scripts.
- These processes should run on identical environment (same release, codebase and config).
- The same dependency isolation techniques should be used for all process types.
- Locally one off scripts can be executed in a shell within the apps directory.
- For production, developers can SSH or use other remote commands to execute the script within the environment.