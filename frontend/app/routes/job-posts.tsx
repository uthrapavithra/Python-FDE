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


export default function JobPosts({ loaderData }) {
  return (
    <div className="flex flex-col items-center mt-10">

      {/* Page Title */}
      <p className="text-4xl font-bold mb-4">{loaderData.jobPosts.title}</p>
      <div className="flex flex-wrap justify-center gap-6">
      {/* List of Job Posts */}
      {loaderData.jobPosts.map((jobPost) => (
        <div
          key={jobPost.id}
          className="w-80 bg-white shadow-lg rounded-xl p-6 border border-gray-200"
        >
          <h1 className="text-2xl font-semibold mb-2">{jobPost.title}</h1>
          <p className="text-gray-700 mb-4">{jobPost.description}</p>

          {/* Apply Button */}
          <Link
            to={`/job-posts/${jobPost.id}/apply`}
            className="block w-full bg-blue-600 text-white text-center py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Apply
          </Link>
        </div>
      ))}
    </div>
    </div>
  );
}