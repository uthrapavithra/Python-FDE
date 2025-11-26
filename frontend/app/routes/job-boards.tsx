
import { Link } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow }  from "~/components/ui/table";
import { Button }  from "~/components/ui/button";
 

export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  console.log(jobBoards)
  return {jobBoards}
}

export default function JobBoards({loaderData}) {
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
        </TableRow>
      </TableHeader>
      <TableBody>
          {loaderData.jobBoards.map(
          (jobBoard) => 
            <TableRow key={jobBoard.id}>
              <TableCell>
                {jobBoard.logo_url
                ?  <Avatar><AvatarImage src={jobBoard.logo_url}></AvatarImage></Avatar>
                : <></>}
              </TableCell>
              <TableCell><Link to={`/job-boards/${jobBoard.id}/job-posts`} className="capitalize">{jobBoard.company_name}</Link></TableCell>
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