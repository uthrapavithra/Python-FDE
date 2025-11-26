// export default function JobBoards(){
//     return (<div>
//     Comingsoon
//   </div>)

import { Link } from "react-router";

        
// }
//const jobPosts= null

export async function clientLoader({params}) {
  const res = await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`);
  const jobPosts = await res.json();
  console.log(jobPosts)
  return {jobPosts}
}



export default function JobPosts({loaderData}) {
    
    

  return (
    
    <div className="flex justify-center items-center">
    
        <p>{loaderData.jobPosts.title}</p>
      {loaderData.jobPosts.map(
        (jobPost) => 
          <div>
            <h1 className="mt-20 text-3xl font-bold" key={jobPost.id}>{jobPost.title}</h1>
            <p>{jobPost.description}</p>
          </div> 
      )}
    </div>
  )
}