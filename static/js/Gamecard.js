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
            let sum = 0;
            let digit = 0;

            for(let num_index=0; num_index<this.numbers.length;num_index++) {
                if (html.id.includes(this.numbers[num_index])) {
                    digit = num_index;
                }
            }

            for (let dice of this.dice.dice_elements) {
                if (dice.src.includes(this.numbers[digit])) {
                    sum += digit; //how many times the category number shows up
                }
            }
            return value == sum; 
        }
        
        if (html.className.includes("lower")) {
            let dice_counts = this.dice.get_counts() //0 index is a rolled 1, 5 index is a rolled 6
            let dice_sum = this.dice.get_sum()
            console.log(dice_sum, dice_counts);

            if (html.id.includes("three")) {
                for (let count_index=0; count_index<dice_counts.length;count_index++) {
                    if (dice_counts[count_index] == 3) {
                        return value == dice_sum; 
                    }
                }
            }
            if (html.id.includes("four")) {
                for (let count_index=0; count_index<dice_counts.length;count_index++) {
                    if (dice_counts[count_index] == 4) {
                        return value == dice_sum;
                    }
                }
            }
            if (html.id.includes("full_house")) {
                if (dice_counts.includes(3) && dice_counts.includes(2)) {
                    return value == 25;
                }
            }
            if (html.id.includes("small")) {
                if (dice_counts.toString().includes('1,1,1')) { //oh... no it can be more than 1, can be 2,1,1
                    return value == 30;
                }
                return false;
            }
            if (html.id.includes("large")) { //can't do == with arrays in javascript
                if (dice_counts.toString().includes('1,1,1,1,1')) {
                    return value == 40;
                } 
                return false;
            }
            if (html.id.includes("yahtzee")) {
                if (dice_counts.indexOf(5) == -1) {
                    return false;
                }
                return value == 50;
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





