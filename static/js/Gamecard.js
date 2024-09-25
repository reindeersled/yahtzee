class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements; //html objects
        this.dice=myDice; //dice
        this.score_elements=score_elements; //td html objects

        this.numbers = ["blank", "one", "two", "three", "four", "five", "six"];
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
        let full = False;
        
        return full;
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
    is_valid_score(category, value){
        let html = document.getElementById(category);

        if (html.className.includes("upper")) { //for upper category
            let category_number = 0;
            let sum = 0;

            for (let number_index=0; number_index<this.numbers.length;number_index++) {
                if (html.id.includes(this.numbers[number_index])) {
                    category_number = number_index;
                }
            }
            for (let dice of this.dice.dice_elements) {
                if (dice.id.includes(category_number)) {
                    sum += category_number;
                }
            }
            return value==sum;
        }
        
        if (html.className.includes("lower")) {
            let dice_counts = this.dice.get_counts()
            let dice_sum = this.dice.get_sum()

            if (html.id.includes("three")) {
                for (let count_index=0; count_index<dice_counts.length;count_index++) {
                    if (dice_counts[count_index] == 3) {
                        return value == count_index * 3; //use if statements again
                    }
                }
            }
            if (html.id.includes("four")) {
                for (let count_index=0; count_index<dice_counts.length;count_index++) {
                    if (dice_counts[count_index] == 4) {
                        return value == count_index * 4; //use if statements again
                    }
                }
            }
            if (html.id.includes("full_house")) {
                if (dice_counts.includes(3) && dice_counts.includes(2)) {
                    if (value == 25) {
                        return true;
                    } else {
                        return false;
                    }
                }
            }

        }
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){

    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       
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
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(score_info){
       
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
      
    }
}

export default Gamecard;





