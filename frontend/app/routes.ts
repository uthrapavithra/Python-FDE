import  { layout, route, type RouteConfig  } from "@react-router/dev/routes";

export default [
    layout("layouts/default.tsx",[
    route("/","routes/home.tsx"),
    route("job-boards","routes/job-boards.tsx"),
    route("job-boards/:jobBoardId/job-posts","routes/job-posts.tsx"),
    route("job-boards/new","routes/new-job-board.tsx"),
    route("job-boards/:jobBoardId/edit","routes/edit-job-board.tsx"),
    route("job-posts/:jobPostId/apply","routes/apply-jobs.tsx")])
] satisfies RouteConfig;
