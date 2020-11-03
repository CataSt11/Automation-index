SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- --------------------------------------------------------

--
-- Table structure for table `automation_tools`
--

CREATE TABLE `automation_tools` (
  `id` int(11) NOT NULL,
  `tool_type` text NOT NULL,
  `system_name` text NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `connections_tasks_automations`
--

CREATE TABLE `connections_tasks_automations` (
  `id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `automation_tool_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `connections_workflows_departments`
--

CREATE TABLE `connections_workflows_departments` (
  `id` int(11) NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `name` text NOT NULL,
  `visibility` enum('enabled','disabled') NOT NULL,
  `order_number` int(11) NOT NULL,
  `time_of_completion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `tasks_executions`
--

CREATE TABLE `tasks_executions` (
  `id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `workflows`
--

CREATE TABLE `workflows` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `automation_tools`
--
ALTER TABLE `automation_tools`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `connections_tasks_automations`
--
ALTER TABLE `connections_tasks_automations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `constraint_automation_tools_id` (`automation_tool_id`),
  ADD KEY `constraint_tasks_id` (`task_id`);

--
-- Indexes for table `connections_workflows_departments`
--
ALTER TABLE `connections_workflows_departments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `constraint_departments_id` (`department_id`),
  ADD KEY `constraint_workflows_id` (`workflow_id`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tasks_executions`
--
ALTER TABLE `tasks_executions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `constraint_task_id_2` (`task_id`);

--
-- Indexes for table `workflows`
--
ALTER TABLE `workflows`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `automation_tools`
--
ALTER TABLE `automation_tools`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `connections_tasks_automations`
--
ALTER TABLE `connections_tasks_automations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `connections_workflows_departments`
--
ALTER TABLE `connections_workflows_departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tasks_executions`
--
ALTER TABLE `tasks_executions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `workflows`
--
ALTER TABLE `workflows`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `connections_tasks_automations`
--
ALTER TABLE `connections_tasks_automations`
  ADD CONSTRAINT `constraint_automation_tools_id` FOREIGN KEY (`automation_tool_id`) REFERENCES `automation_tools` (`id`),
  ADD CONSTRAINT `constraint_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`);

--
-- Constraints for table `connections_workflows_departments`
--
ALTER TABLE `connections_workflows_departments`
  ADD CONSTRAINT `constraint_departments_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
  ADD CONSTRAINT `constraint_workflows_id` FOREIGN KEY (`workflow_id`) REFERENCES `workflows` (`id`);

--
-- Constraints for table `tasks_executions`
--
ALTER TABLE `tasks_executions`
  ADD CONSTRAINT `constraint_task_id_2` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`);
COMMIT;
