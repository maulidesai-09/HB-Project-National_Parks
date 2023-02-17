// React for Review Comments

function ReviewComment(props) {
    return (
        <div className="comment">
            <br></br>
            <p> {props.review} </p>
            <br></br>
            <p> By: {props.user} </p>
            <p> -------------------------------------------------------------------------------------- </p>

        </div>
    )
}



function AddReviewComment(props) {
    // const [id, setId] = React.useState("")
    const[review, setReview] = React.useState("")
    // const[user, setUser] = React.useState("")

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
            <br></br>
            <b> Add New Review: </b>
            <br></br>
            <label htmlFor="reviewInput"> Review </label>
            <textarea
            value={review}
            onChange={(event) => setReview(event.target.value)}
            id="reviewInput"
            wrap="hard" 
            style={{ width: "500px", height: "200px" }}
            ></textarea>

            <button style={{ marginLeft: "10px" }} onClick={addNewReviewComment}>
                Add
            </button>
        </React.Fragment>
    )
}







function ReviewCommentContainer() {

    // const reviewComment = {
    //     review: "Sample review comment hard coded",
    //     user: "Sample User"
    // };

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
            <b> Reviews: </b>
            <br></br>
            <div className="review_comments_css"> {reviewComments} </div>
            <AddReviewComment addComment={addComment}/>
        </React.Fragment>
    )
}

ReactDOM.render(<ReviewCommentContainer />, document.getElementById("react_container"))