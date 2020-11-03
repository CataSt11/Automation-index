$(document).ready(function(){

    $(".department-textbox, .btn-func-apply").hide();

    $(".btn-func-edit").click(function(){
        var $elemId = $(this).attr("id").split("_")[1]
        $("#department_textbox_" + $elemId + ", #apply_" + $elemId).show();
        $("#department_text_" + $elemId + ", #edit_" + $elemId + ", #delete_" + $elemId).hide();
        console.log("Button edit id = " + $elemId + " clicked.");
    });

    $(".btn-func-apply").click(function(){
        var $elemId = $(this).attr("id").split("_")[1]
        var $elemValue = $("#department_textbox_" + $elemId).val()
        $.ajax({
            url: '/database/departments',
            type: 'patch',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                console.log("The update operation was successful");
                location.reload();
            },
            error: function(data) {
                console.log("The update operation resulted in an error");
            },
            data: JSON.stringify({ department_id: $elemId, department_name: $elemValue })
        });

        $("#department_textbox_" + $elemId + ", #apply_" + $elemId).hide();
        $("#department_text_" + $elemId + ", #edit_" + $elemId + ", #delete_" + $elemId).show();
        $("#department_text_" + $elemId).text($elemValue);
    });

    $(".btn-func-delete").click(function(){
        var $elemId = $(this).attr("id").split("_")[1]
        $.ajax({
            url: '/database/departments',
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
            data: JSON.stringify({ department_id: $elemId })
        });
    });

    $("#add_button").click(function(){
        var $elemValue = $("#new_department").val()
        $.ajax({
            url: '/database/departments',
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
            data: JSON.stringify({ department: $elemValue })
        });
    });

});
