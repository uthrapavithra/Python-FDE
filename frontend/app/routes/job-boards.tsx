// export default function JobBoards(){
//     return (<div>
//     Comingsoon
//   </div>)

import { Link } from "react-router";

        
// }

export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
}

export default function JobBoards({loaderData}) {
    // return <p>{loaderData.jobBoards.length}</p>

    console.log(loaderData.jobBoards)

    return (
        <div>
            
        {loaderData.jobBoards.map(
            (jobBoard) => 
            <p key={jobBoard.id}>
                <Link to={`/job-boards/${jobBoard.id}/job-posts`}>{jobBoard.company_name}</Link>
                
                { jobBoard.logo_url 
                ? <img src={jobBoard.logo_url} width="100" height="100" ></img>
            : <></>
        }
            </p>
        )}
        </div>
    )
}