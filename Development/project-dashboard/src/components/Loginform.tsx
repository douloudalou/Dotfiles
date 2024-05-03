"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }).regex(/^[A-Za-z]+$/, {
    message: "Username must contain only letters.",
  }),
})

export const LoginForm = () => {
  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
    },
  })

  const router = useRouter()

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    alert(JSON.stringify(values))
  }
  useEffect(() => {
    if (form.formState.isSubmitSuccessful) {
      router.push("/landing");
    }
  }, [form.formState.isSubmitSuccessful, router]);

  // Form Appearance
  return (
    <div>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Username</FormLabel>
                <FormControl>
                  <Input placeholder="Meee" {...field}/>
                </FormControl>
                <FormDescription>
                  This is your public display name.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit">Submit</Button>
        </form>
      </Form>
    </div>
  )
}
