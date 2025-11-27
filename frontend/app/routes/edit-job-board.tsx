import { Form, Link, redirect, useLoaderData } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";

export async function clientLoader({params} : Route.ClientLoaderArgs) {
  const res = await fetch(`/api/job-boards/${params.jobBoardId}`)
  const jobBoard = await res.json()
  console.log("inside loader")
  console.log(jobBoard)
  return {jobBoard}
}


export async function clientAction({request,params}:Route.ClientActionArgs) {
    
    const formData = await request.formData()
    // const formValues = Object.fromEntries(formData);
    console.log("FORMMMMM ---- ",params.jobBoardId);
    await fetch(`/api/job-boards/${params.jobBoardId}`,{
        method: 'PUT',
        body: formData,
        })
    return redirect('/job-boards')
  
}


export default function EditJobBoardForm({loaderData}: Route.ComponentProps) {
    //const loaderData = useLoaderData<typeof clientLoader>();
    console.log("Loder----",loaderData.jobBoard)
  return (
    <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
      <input type="hidden" name="job_board_id" value={loaderData.jobBoard.id} /> 
        <FieldGroup>
          <FieldLegend>Edit Job Board</FieldLegend>
          <Field>
            <FieldLabel htmlFor="company_name">
              Company Name
            </FieldLabel>
            <Input
              id="company_name"
              name="company_name"
              defaultValue={loaderData.jobBoard.company_name}
              
              
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="logo">
              Logo
            </FieldLabel>
            <Input
              id="logo"
              name="logo"
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