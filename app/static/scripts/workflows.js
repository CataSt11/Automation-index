function parseTasks(workflowId) {
    var taskElements = []
    $("#workflows_tasks_container-" +  workflowId).children().each( function(index1, this1){
        if ($(this1).attr("id") != undefined && $(this1).attr("id").startsWith("workflows_workflow" +  workflowId + "_group_task_elements_container-")) {
            taskId = $(this1).attr("id").split("-")[1]
            taskElements.push({"id": taskId});
            $(this1).children().each( function(index2, this2){
                if ($(this2).attr("class").split(" ").includes("workflows-group-task-name-textbox--" +  workflowId)) {
                    taskElements[taskElements.length - 1]["name"] = $(this2).val();
                }
                if ($(this2).attr("class").split(" ").includes("workflows-group-timecomp-textbox--" +  workflowId)) {
                    taskElements[taskElements.length - 1]["time_of_completion"] = $(this2).val();
                }
                if ($(this2).attr("class").split(" ").includes("workflows-group-task-automation-tool-select--" +  workflowId)) {
                    taskElements[taskElements.length - 1]["automation_tool_id"] = $(this2).val();
                }
            });
        }
    });
    return taskElements;
}

function setArrowButtonsStatus(workflowId) {
    taskElements = parseTasks(workflowId)
    selectedTaskId = $("input:radio.workflows-radio-order--" + workflowId + ":checked").val()
    radioBtnIdx = taskElements.findIndex(function(currentValue){return currentValue["id"] == selectedTaskId;})
    if (radioBtnIdx == 0) {
        $("#workflows_up_btn-" +  workflowId).attr("src", "static/images/up-disabled.gif")
        $("#workflows_up_btn-" +  workflowId).css("cursor", "auto")
        $("#workflows_down_btn-" +  workflowId).attr("src", "static/images/down-enabled.gif")
        $("#workflows_down_btn-" +  workflowId).css("cursor", "pointer")
    }
    if (radioBtnIdx >= 1 && radioBtnIdx <= taskElements.length - 2) {
        $("#workflows_up_btn-" +  workflowId).attr("src", "static/images/up-enabled.gif")
        $("#workflows_up_btn-" +  workflowId).css("cursor", "pointer")
        $("#workflows_down_btn-" +  workflowId).attr("src", "static/images/down-enabled.gif")
        $("#workflows_down_btn-" +  workflowId).css("cursor", "pointer")
    }
    if (radioBtnIdx == taskElements.length - 1) {
        $("#workflows_up_btn-" +  workflowId).attr("src", "static/images/up-enabled.gif")
        $("#workflows_up_btn-" +  workflowId).css("cursor", "pointer")
        $("#workflows_down_btn-" +  workflowId).attr("src", "static/images/down-disabled.gif")
        $("#workflows_down_btn-" +  workflowId).css("cursor", "auto")
    }
}

$(document).ready(function(){

    $(".workflows-tasks-edit").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        var showElements = []
        showElements.push(".workflows-group-remove-task--" +  workflowId)
        showElements.push(".workflows-group-tasks-details-edit--" +  workflowId)
        showElements.push(".workflows-group-tasks-add-text--" +  workflowId)
        showElements.push(".workflows-group-tasks-add--" +  workflowId)
        showElements.push(".workflows-group-tasks-cancel-changes--" +  workflowId)
        $(showElements.join(", ")).show();

        var hideElements = []
        hideElements.push(".workflows-group-tasks-edit--" +  workflowId)
        $(hideElements.join(", ")).hide();

        console.log("'Edit tasks' button was clicked.")
    });


    $(".workflows-remove-task").click(function(){
        var taskId = $(this).attr("id").split("-")[1]
        var payload = {"id": taskId}
        $.ajax({
            url: '/database/tasks',
            type: 'delete',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The delete operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The delete operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        location.reload();
    });

    $(".workflows-tasks-add-button").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        taskName = $("#workflows_tasks_add_text-" + workflowId).val()
        var payload = {"name": taskName, "workflow_id":workflowId}
        $.ajax({
            url: '/database/tasks',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The add operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The add operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        location.reload();
    });

    $(".workflows-tasks-cancel-changes").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        var hideElements = []
        hideElements.push(".workflows-group-remove-task--" +  workflowId)
        hideElements.push(".workflows-group-tasks-details-edit--" +  workflowId)
        hideElements.push(".workflows-group-tasks-apply--" +  workflowId)
        hideElements.push(".workflows-group-tasks-add-text--" +  workflowId)
        hideElements.push(".workflows-group-tasks-add--" +  workflowId)
        hideElements.push(".workflows-group-tasks-cancel-changes--" +  workflowId)
        hideElements.push(".workflows-group-task-name-textbox--" +  workflowId)
        hideElements.push(".workflows-group-timecomp-textbox--" +  workflowId)
        hideElements.push(".workflows-group-remove-task--" +  workflowId)
        hideElements.push(".workflows-group-task-automation-tool-select--" +  workflowId)
        hideElements.push(".workflows-radio-order--" +  workflowId)
        hideElements.push(".workflows-change-order-buttons--" +  workflowId)
        $(hideElements.join(", ")).hide();

        var showElements = []
        showElements.push(".workflows-group-tasks-edit--" +  workflowId)
        showElements.push(".workflows-group-task-name-text--" +  workflowId)
        showElements.push(".workflows-group-timecomp-text--" +  workflowId)
        $(showElements.join(", ")).show();
        console.log("'Cancel changes' button was clicked.")
    });

    $(".up-btn, .down-btn").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        taskElements = parseTasks(workflowId)
        selectedTaskId = $("input:radio.workflows-radio-order--" + workflowId + ":checked").val()
        radioBtnIdx = taskElements.findIndex(function(currentValue){return currentValue["id"] == selectedTaskId;})
        if ($(this).attr("src") == "static/images/up-enabled.gif") {
            previousTaskId = taskElements[radioBtnIdx - 1]["id"]
            $("#workflows_workflow" + workflowId + "_group_task_elements_container-" + selectedTaskId).insertBefore($("#workflows_workflow" + workflowId + "_group_task_elements_container-" + previousTaskId))
        }
        if ($(this).attr("src") == "static/images/down-enabled.gif") {
            nextTaskId = taskElements[radioBtnIdx + 1]["id"]
            $("#workflows_workflow" + workflowId + "_group_task_elements_container-" + selectedTaskId).insertAfter($("#workflows_workflow" + workflowId + "_group_task_elements_container-" + nextTaskId))
        }
        setArrowButtonsStatus(workflowId)
    });

    $(".workflows-radio-btn").click(function(){
        var workflowId = $(this).attr("class").split("--")[1]
        setArrowButtonsStatus(workflowId)
    });
    
    $(".workflows-tasks-details-edit").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        var hideElements = []
        hideElements.push(".workflows-group-task-name-text--" +  workflowId)
        hideElements.push(".workflows-group-timecomp-text--" +  workflowId)
        hideElements.push(".workflows-group-task-automation-tool-text--" +  workflowId)
        hideElements.push(".workflows-group-remove-task--" +  workflowId)
        hideElements.push(".workflows-group-tasks-details-edit--" +  workflowId)
        hideElements.push(".workflows-group-tasks-add-text--" +  workflowId)
        hideElements.push(".workflows-group-tasks-add--" +  workflowId)
        $(hideElements.join(", ")).hide();

        var showElements = []
        showElements.push(".workflows-group-tasks-apply--" +  workflowId)
        showElements.push(".workflows-group-task-name-textbox--" +  workflowId)
        showElements.push(".workflows-group-timecomp-textbox--" +  workflowId)
        showElements.push(".workflows-group-task-automation-tool-select--" +  workflowId)
        showElements.push("#workflows_down_btn-" +  workflowId)
        showElements.push("#workflows_up_btn-" +  workflowId)
        showElements.push(".workflows-radio-order--" +  workflowId)
        $(showElements.join(", ")).show();

        console.log("'Edit task-name' button was clicked.")
    });

    $(".workflows-tasks-apply").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        payload = parseTasks(workflowId)
        $.ajax({
            url: '/database/tasks',
            type: 'patch',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The add operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The add operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        console.log("Sending the following payload to /database/update/task")
        console.log(payload)
        
    });

    $(".workflows-btn-func-workflow-edit").click(function($event){
        $event.stopPropagation()
        var workflowId = $(this).attr("id").split("-")[1]
        var showElements = []
        showElements.push("#workflows_workflow_textbox-" +  workflowId)
        showElements.push("#workflows_btn_func_workflow_apply-" +  workflowId)
        $(showElements.join(", ")).show();

        var hideElements = []
        hideElements.push("#workflows_workflow_text-" +  workflowId)
        hideElements.push("#workflows_btn_func_workflow_edit-" +  workflowId)
        hideElements.push("#workflows_btn_func_workflow_delete-" +  workflowId)
        $(hideElements.join(", ")).hide();
    });

    $(".workflows-btn-func-workflow-apply").click(function($event){
        $event.stopPropagation()
        var workflowId = $(this).attr("id").split("-")[1]
        var workflowValue = $("#workflows_workflow_textbox-" +  workflowId).val()
        var payload = {"id": workflowId, "name": workflowValue}
        $.ajax({
            url: '/database/workflows',
            type: 'patch',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The edit operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The edit operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        location.reload();
    });

    $(".workflows-btn-func-workflow-delete").click(function($event){
        $event.stopPropagation()
        var workflowId = $(this).attr("id").split("-")[1]
        var payload = {"id": workflowId}
        $.ajax({
            url: '/database/workflows',
            type: 'delete',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The add operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The add operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        location.reload();
    });

    $("#workflows_add_workflow_button").click(function(){
        var workflowName = $("#workflows_new_workflow").val()
        var payload = {"name": workflowName}
        $.ajax({
            url: '/database/workflows',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The add operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The add operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
        location.reload();
    });

    $(".workflows-workflow-title").click(function(){
        var elemId = $(this).attr("id").split("-")[1]
        console.log(this.id)
        $("#workflows_group_wt-" + elemId).toggle();
    });
        
    $(".workflow-departments-tab").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        $("#workflows_group_wt-" + workflowId).show();
        $("#workflows_departments_container-" + workflowId).show();
        $("#workflows_tasks_container-" + workflowId).hide();
        $("#workflow_tasks_tab-" + workflowId).css({"background-color": "white", "color": "black"})
        $("#workflow_departments_tab-" + workflowId).css({"background-color": "#AED1D5", "color": "white"})
    });

    $(".workflow-tasks-tab").click(function(){
        var workflowId = $(this).attr("id").split("-")[1]
        $("#workflows_group_wt-" + workflowId).show();
        $("#workflows_departments_container-" + workflowId).hide();
        $("#workflows_tasks_container-" + workflowId).show();
        $("#workflow_tasks_tab-" + workflowId).css({"background-color": "#AED1D5", "color": "white"})
        $("#workflow_departments_tab-" + workflowId).css({"background-color": "white", "color": "black"})
    });

    $(".workflows-departments-remove").click(function(){
        var workflowId = $(this).attr("class").split("--")[1]
        var departmentId = $(this).attr("id").split("-")[1]
        payload = {"workflow_id": workflowId, "department_id": departmentId}
        $.ajax({
            url: '/database/workflows-associations',
            type: 'delete',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The delete operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The delete operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
    })

    $(".workflows-departments-assign").click(function(){
        workflowId = $(this).attr("id").split("-")[1]
        departmentId = $("#workflows_select_new_department-" + workflowId).val()
        payload = {"workflow_id": workflowId, "department_id": departmentId}
        $.ajax({
            url: '/database/workflows-associations',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The post operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The post operation resulted in an error");
            },
            data: JSON.stringify(payload)
        });
    })

});
