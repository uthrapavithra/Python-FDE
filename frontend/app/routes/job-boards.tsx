
import { Link, useFetcher } from "react-router";
import type { Route } from "../+types/root";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow }  from "~/components/ui/table";
import { Button }  from "~/components/ui/button";
 

export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  console.log("jobboards---",jobBoards)
  return {jobBoards}
}

export async function clientAction({request}: Route.ClientActionArgs) {
    const formData = await request.formData()
    const jobBoardId = formData.get('job_board_id')
    await fetch(`/api/job-boards/${jobBoardId}`,{
        method:'DELETE'
    })
  
}

export default function JobBoards({loaderData} : any) {
    const fetcher = useFetcher();
  return (
    <div>
    <div>
        <Button>
        <Link to ="/job-boards/new">Add New Job board</Link>
      </Button>
    </div>
    
    <div className="flex justify-center items-center">
        
    <Table className="w-1/2 bg-white shadow rounded-lg">
      <TableHeader>
        <TableRow>
          <TableHead>Logo</TableHead>
          <TableHead>Company</TableHead>
          <TableHead></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
            
          {// @ts-ignore
          loaderData.jobBoards.map(
            // @ts-ignore
          (jobBoard) => 
            <TableRow key={jobBoard.id}>
              <TableCell>
                {jobBoard.logo_url
                ?  <Avatar><AvatarImage src={jobBoard.logo_url}></AvatarImage></Avatar>
                : <></>}
              </TableCell>
              <TableCell><Link to={`/job-boards/${jobBoard.id}/job-posts`} className="capitalize">{jobBoard.company_name}</Link></TableCell>
              <TableCell><Link to={`/job-boards/${jobBoard.id}/edit`} className="capitalize">Edit</Link></TableCell>
              
              <TableCell>
                <fetcher.Form method="post"
                    onSubmit={(event) => {
                      const response = confirm(
                        `Please confirm you want to delete this job board '${jobBoard.company_name}'.`,
                      );
                      if (!response) {
                        event.preventDefault();
                      }
                    }}>
                    <input name="job_board_id" type="hidden" value={jobBoard.id}></input>
                    <button>Delete</button>
                  </fetcher.Form>
              </TableCell>
            </TableRow>
        )}
      </TableBody>
    </Table>
    </div>
    </div>
  )
}

// export default function JobBoards({loaderData}) {
//     // return <p>{loaderData.jobBoards.length}</p>

//     console.log(loaderData.jobBoards)

//     return (
//         <div>
            
//         {loaderData.jobBoards.map(
//             (jobBoard) => 
//             <p key={jobBoard.id}>
//                 <Link to={`/job-boards/${jobBoard.id}/job-posts`}>{jobBoard.company_name}</Link>
                
//                 { jobBoard.logo_url 
//                 ? <img src={jobBoard.logo_url} width="100" height="100" ></img>
//             : <></>
//         }
//             </p>
//         )}
//         </div>
//     )
// }