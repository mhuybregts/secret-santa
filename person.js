class Person {
    constructor(name, email, exclude) {
        
        this.name = name;
        this.email = email;

        if (exclude == '') {
            this.exclude = new Array();
        }
        else if (Array.isArray(exclude)) {
            this.exclude = exclude;
        } else {
            this.exclude = exclude.split(',');
        }
        this.available = true;
        this.match = null;
    }
}