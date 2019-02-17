    var counter = 0;
    function moreFields() {
        counter++;
        var newFields       = document.getElementById('readroot').cloneNode(true);
        var newFields_range = document.getElementById('readroot_range').cloneNode(true);
        var newFields_inf   = document.getElementById('readroot_inf').cloneNode(true);
        newFields.id = '';
        newFields_range.id = '';
        newFields_inf.id = '';
        newFields.style.display = 'block';
        newFields_range.style.display = 'block';
        newFields_inf.style.display = 'block';
        var newField = newFields.childNodes;
        var newField_range = newFields_range.childNodes;
        var newField_inf = newFields_inf.childNodes;
        for (var i=0;i<newField.length;i++) {
            var theName = newField[i].name
                if (theName)
                    newField[i].name = theName + counter;
        }
        var insertHere = document.getElementById('writeroot');
        insertHere.parentNode.insertBefore(newFields,insertHere);
        for (var i=0;i<newField_range.length;i++) {
            var theName_range = newField_range[i].name
                if (theName_range)
                    newField_range[i].name = theName_range + counter;
        }
        var insertHere_range = document.getElementById('writeroot_range');
        insertHere_range.parentNode.insertBefore(newFields_range,insertHere_range);
        for (var i=0;i<newField_inf.length;i++) {
            var theName_inf = newField_inf[i].name
                if (theName_inf)
                    newField_inf[i].name = theName_inf + counter;
        }
        var insertHere_inf = document.getElementById('writeroot_inf');
        insertHere_inf.parentNode.insertBefore(newFields_inf,insertHere_inf)
    }
    function toggleA(button) {
        var arbutton = document.getElementById("ar");
        if(arbutton.disabled) {
          button.value = "Remove Annotation";
          arbutton.disabled = false;
          $('.annotations').show();
          $('#anno').val("1");
        } else {
          button.value = "Add Annotation";
          arbutton.disabled = true;
          $('.annotations').hide();
          $('#anno').val("0");
        }
    }

