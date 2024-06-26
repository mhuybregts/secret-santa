$(document).ready(function(){

    Sortable.create(document.getElementById('people'));
    
    $('#num-people').on('change', function(){
        
        let numPeople = $(this).val();
        if (numPeople == 0) {
            $(this).val('1');
            return;
        }

        let i = 1;
        $('.person-row').each(function(){
            if (numPeople < i) {
                $(this).remove();
            }
            i++;
        });

        let rowCopy = $('.person-row:first').clone();
        while (i <= numPeople) {
            if (i % 2 == 0) {
                rowCopy.addClass('even');
            } else {
                rowCopy.addClass('odd');
            }
            rowCopy.find('[name=name]').val('');
            rowCopy.find('[name=email]').val('');
            rowCopy.find('[name=exclude]').val('');
           
            $('#people').append(rowCopy);
            i++;
        }
    });

    $('#generate-pairs').on('click', function(){

        $('#response-modal .modal-title').text('SECRET SANTA');
        $('#response-modal .modal-body').text('Generating Pairs');
        $('<div/>',{ id: 'loading',class: 'spinner-border'}).appendTo('#response-modal .modal-body');
        $('#response-modal').modal('show');
        
        var people = new Array();
        var validated = true;
        
        // Iterate through each row and create a person object
        $('.person-row').each(function(){
        
            let name = $(this).find('[name=name]').val();
            let email = $(this).find('[name=email]').val();
            let exclude = $(this).find('[name=exclude]').val();

            console.log(name)
            console.log(email)

            if (name.length == 0 || email.length == 0) {
                validated = false;
                return;
            }

            let person = new Person(name, email, exclude);
            people.push(person);

        });

        if (!validated) {
            $('#response-modal .modal-body').text('Make sure everyone has a name and email!');
            $('#loading').remove();
            return false;
        }

        // Iterate through array    
        var peopleLength = people.length;
        for (let i=0; i < peopleLength; i++) {

            var person = people.splice(i, 1)[0];
            
            var index = Math.floor(Math.random() * (peopleLength - 1));
            var originalIndex = index;
            var valid = false;

            do {
                let match = people[index];
                if (!match.available || person.exclude.includes(match.name)) {
                    index = (index + 1) % (peopleLength - 1);
                    if (index == originalIndex) {
                        $('#response-modal .modal-title').text('OOPS!')
                            .removeClass('text-success')
                            .addClass('text-danger');

                        $('#response-modal .modal-body').text('Looks like we couldn\'t get a match for everyone. Try Again.')
                            .append('<br><small><b>TIP: Put the people who can\'t match with other people at the top</b></small>');
                        
                        return false;
                    }
                } else {
                    match.available = false;
                    valid = true;
                    person.match = match;
                }

            } while (!valid);

            people.splice(i, 0, person);
        }

        let sent = true;

        // Send emails 
        people.forEach(function(person) {
            
            let data = new URLSearchParams();
            data.append('person', person.name);
            data.append('address', person.email);
            data.append('match', person.match.name);

            fetch('http://localhost:9000/send_email', {
                method: 'POST',
                body: data
            })
            .then(response => response.text())
            .then(data => {
                console.log('Response:', data);
            })
            .catch(error => {
                console.error('Error:', error);
                sent = false;
                return;
            });
        });

        if (!sent) {
            alert('Server unable to send all emails');
            return false;
        }

        $('#response-modal .modal-title').text('SUCCESS!')
            .removeClass('text-danger')
            .addClass('text-success');

        $('#response-modal .modal-footer small').remove();
        $('#response-modal .modal-body').text('Everyone has gotten a match, check your email to see who you got.');

    });
});