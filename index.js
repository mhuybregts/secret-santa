$(document).ready(function(){

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

        var people = new Array();
        
        // Iterate through each row and create a person object
        $('.person-row').each(function(){
        
            let name = $(this).find('[name=name]').val();
            let email = $(this).find('[name=email]').val();
            let exclude = $(this).find('[name=exclude]').val();

            if (name.length == 0 || email.length == 0) {
                return false;
            }

            let person = new Person(name, email, exclude);
            people.push(person);

        });

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
                        $('#error-modal').modal('show');
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

        // Send emails 
        people.forEach(function(person) {
            
            let message = `
            Hello ${person.name}, 
            
            You have gotten ${person.match.name} for Secret Santa!
            Remember to keep it a secret (and get a good gift).
            
            Merry Christmas!`


            var data = new URLSearchParams();
            data.append('recipient', person.email);
            data.append('message', message);

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
            });
        });
    });
});