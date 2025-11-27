import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";

// export async function clientLoader({params} : Route.ClientLoaderArgs) {
//   const res = await fetch(`/api/job-posts/${params.jobPostId}`)
//   const jobPost = await res.json()
  
//   console.log(jobPost)
//   return {jobPost}
// }

export async function clientAction({request}:Route.ClientActionArgs) {
    const formData = await request.formData()
    const formvalues= Object.fromEntries(formData)
    console.log(formvalues)
    await fetch('/api/job-applications',{
        method: 'POST',
        body: formData,
        })
    return redirect('/job-boards')
  
}

export default function NewJobPostForm({loaderData,params}: Route.ComponentProps) {
    console.log("id---",params.jobPostId)
  return (
    <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
      
        <FieldGroup>
          <FieldLegend>Apply for the Job</FieldLegend>
          <Field>
            <FieldLabel htmlFor="job_post_id">
              Job ID
            </FieldLabel>
            <Input
              id="job_post_id"
              name="job_post_id"
              value={params.jobPostId}
              placeholder={params.jobPostId}
              readOnly
    
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="first_name">
              First Name
            </FieldLabel>
            <Input
              id="first_name"
              name="first_name"
              required
              
              
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="last_name">
              Last Name
            </FieldLabel>
            <Input
              id="last_name"
              name="last_name"
              required
              
              
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="email">
              Email
            </FieldLabel>
            <Input
              id="email"
              type="email"
              name="email"
              required
              
              
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="resume">
              Resume
            </FieldLabel>
            <Input
              id="resume"
              name="resume"
              type="file"
              
            />
          </Field>
          <div className="float-right">
            <Field orientation="horizontal">
              <Button type="submit">Submit</Button>
              <Button variant="outline" type="button">
                <Link to="/job-boards">Cancel</Link>
              </Button>
            </Field>
          </div>
        </FieldGroup>
      </Form>
    </div>
  );
}