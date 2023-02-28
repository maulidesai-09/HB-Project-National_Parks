// React for Review Comments

function ReviewComment(props) {
    return (
        <div className="comment">
            <p className="comment-text"> {props.review} </p>
            <br></br>
            <p className="comment-text"> <b> By: {props.user} </b></p>

        </div>
    )
}



function AddReviewComment(props) {
    const[review, setReview] = React.useState("")

    function addNewReviewComment(){
        fetch("/add-review-comment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"review": review, "park_id": document.querySelector("#park_id").innerHTML})
        })
        .then((response) => response.json())
        .then((jsonResponse) => {
            const reviewAdded = jsonResponse.response
            props.addComment(reviewAdded)
            alert('Review added!')
        })
        
    }
    return (
        <React.Fragment>
            <br></br>
            <b> Add New Review: </b>
            <br></br>
            <label htmlFor="reviewInput"></label>
            <textarea
            value={review}
            onChange={(event) => setReview(event.target.value)}
            id="reviewInput"
            wrap="hard" 
            style={{ width: "500px", height: "200px" }}
            ></textarea>
            <br></br>

            <button class="btn btn-success" onClick={addNewReviewComment}>
                Submit Review
            </button>
        </React.Fragment>
    )
}


function ReviewCommentContainer() {

    const [comments, setComments] = React.useState([])

    function addComment(newReviewComment) {
        const currentComments = [...comments]
        setComments([...currentComments, newReviewComment])
    }

    React.useEffect(() => {
        const park_id = document.querySelector("#park_id").innerHTML
        const url = `/parks/${park_id}/review-comments`

        fetch(url)
        .then((response) => response.json())
        .then((responseJson) => setComments(responseJson.review_comments))
    }, [])

    const reviewComments = []


    for (const currentComment of comments) {
        reviewComments.push(
            <ReviewComment
            key={currentComment.id}
            review={currentComment.review}
            user={currentComment.user}
            />
        )
    }

    return (
        <React.Fragment>
            <h4> Reviews: </h4>
            <div className="review_comments_css"> {reviewComments} </div>
            <AddReviewComment addComment={addComment}/>
        </React.Fragment>
    )
}

ReactDOM.render(<ReviewCommentContainer />, document.getElementById("react_container"))