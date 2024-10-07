class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements; //the html inputs
        this.dice=myDice; //dice
        this.score_elements=score_elements; //the sum stuff, no text boxes

        this.numbers = ["blank", "one", "two", "three", "four", "five", "six"];
        this.upper_categories = ["one","two","three","four","five","six"];
        this.lower_categories = ["three_of_a_kind","four_of_a_kind","full_house","small_straight","large_straight","yahtzee","chance"];
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
        for (let category of this.category_elements) {
            if (!category.hasAttribute("disabled")) {
                return false;
            }
        }
        return true;
    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){ //also disables category if valid
        let html = document.getElementById(category + "_input");
        let dice_ints = this.dice.get_values();
        
        if (dice_ints.indexOf(0) != -1) {
            return false;
        }
        if (typeof value == "string") {
            return false;
        }
        if (value < 0) {
            return false;
        }

        if (html.className.includes("upper")) { //for upper category
            let sum = 0;
            let digit = 0;

            for(let num_index=0; num_index<this.numbers.length;num_index++) { //converting letter number to int number
                if (html.id.includes(this.numbers[num_index])) {
                    digit = num_index;
                }
            }

            for (let dice of this.dice.dice_elements) {
                if (dice.src.includes(this.numbers[digit])) {
                    sum += digit; 
                }
            }

            if (value == sum) {
                html.setAttribute("disabled", "");
                return true;
            }
            return false; 
        }
        
        if (html.className.includes("lower")) {
            let dice_counts = this.dice.get_counts(); //0 index is a rolled 1, 5 index is a rolled 6
            let dice_sum = this.dice.get_sum();
            let dice_values = this.dice.get_values(); //[1, 1, 1, 1, 1]

            if (html.id.includes("three")) {
                if (dice_counts.indexOf(3) != -1 || dice_counts.indexOf(4) != -1 || dice_counts.indexOf(5) != -1) {
                    if (value == dice_sum || value == 0) {
                        html.setAttribute("disabled", "");
                        return true;
                    }
                }
                return value == 0;
            }
            if (html.id.includes("four")) {
                if (dice_counts.indexOf(4) != -1 || dice_counts.indexOf(5) != -1) {
                    if (value == dice_sum || value == 0) {
                        html.setAttribute("disabled", "");
                        return true;
                    }
                }
                return value == 0;
            }
            if (html.id.includes("full_house")) {
                if (dice_counts.includes(3) && dice_counts.includes(2)) {
                    if (value == 25 || value == 0) {
                        html.setAttribute("disabled", "");
                        return true;
                    }
                }
                return value == 0;
            }
            if (html.id.includes("small")) {
                for (let i=0;i<dice_counts.length-2;i++) {
                    if (dice_counts[i] > 0 && dice_counts[i+1] > 0 && dice_counts[i+2] > 0) {
                        if (value == 30 || value == 0) {
                            html.setAttribute("disabled", "");
                            return true;
                        }
                    }
                }
                return value == 0;
            }
            if (html.id.includes("large")) { //can't do == with arrays in javascript
                if (dice_counts.toString().includes('1,1,1,1,1')) {
                    if (value == 40 || value == 0) {
                        html.setAttribute("disabled", "");
                        return true;
                    }
                } 
                return value == 0;
            }
            if (html.id.includes("yahtzee")) {
                if (dice_counts.indexOf(5) != -1) {
                    if (value == 50 || value == 0) {
                        html.setAttribute("disabled", "");
                        return true;
                    }
                }
                return value == 0;
            }
            if (html.id.includes("chance")) {
                if (value == dice_sum || value == 0) {
                    html.setAttribute("disabled", "");
                    return true;
                }
                return false;
            }
        }
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the current game score
    */
    get_score(){
        return parseInt(document.getElementById("grand_total").innerText);
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       let upper_sum = 0;
       let lower_sum = 0;
       let bonus = 0;

       for (let category of this.category_elements) {
            if (category.hasAttribute("disabled")) {
                if (category.className.includes("upper")) {
                    upper_sum += Number(category.value);
                }
                if (category.className.includes("lower")) {
                    lower_sum += Number(category.value);
                }
            }
       }
       document.getElementById("upper_score").innerHTML = upper_sum;
       if (upper_sum > 63) {
            bonus = 35;
            document.getElementById("upper_bonus").innerHTML = 35;
       }
       document.getElementById("upper_total").innerHTML = upper_sum + bonus;

       document.getElementById("lower_score").innerHTML = lower_sum;
       document.getElementById("upper_total_lower").innerHTML = upper_sum + bonus;
       document.getElementById("grand_total").innerHTML = upper_sum + lower_sum + bonus;
       
    }

    /**
     * Loads a scorecard from a JS object in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} score_info the object version of the scorecard 
    */
    load_scorecard(score_info){ //score info IS gameObject...
        //javascript error: score_info is not iterable

        document.getElementById("rolls_remaining").innerHTML = score_info.rolls_remaining;

        for (let category of this.upper_categories) {
            if (score_info["upper"][category] == -1) {
                document.getElementById(category + '_input').removeAttribute("disabled")
            } else {
                document.getElementById(category + '_input').value = score_info["upper"][category];
                document.getElementById(category + '_input').setAttribute("disabled", "")
            }
        }

        for (let category of this.lower_categories) {
            if (score_info["lower"][category] == -1) {
                document.getElementById(category + '_input').removeAttribute("disabled")
            } else {
                document.getElementById(category + '_input').value = score_info["lower"][category];
                document.getElementById(category + '_input').setAttribute("disabled", "")
            }
        }
    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */
    to_object(){
        let scorecard = { //-1 is no value yet
            "rolls_remaining": 3,
            "upper": {
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower": {
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
        if (document.getElementById("rolls_remaining").innerHTML != null) {
            scorecard["rolls_remaining"] = Number(document.getElementById("rolls_remaining").innerHTML);
        }
        for (let upper of this.upper_categories) {
            if (Number.isInteger(document.getElementById(upper + "_input").value)) {
                scorecard["upper"][upper] = Number(document.getElementById(upper + "_input").value);
            }
        }
        for (let lower of this.lower_categories) {
            if (Number.isInteger(document.getElementById(lower + "_input").value)) {
                scorecard["lower"][lower] = Number(document.getElementById(lower + "_input").value);
            }
        }
        return scorecard;
    }
}

export default Gamecard;





