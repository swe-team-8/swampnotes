"use client";
import { useEffect, useState } from "react";
import { useSignIn } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function CustomSignInForm(){
    //values from clerk 
    const {isLoaded, signIn, setActive} = useSignIn();

    //variables that the user will type in 
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const router = useRouter();

    //Handling sign in submission 
    const handleSubmit = async (e: React.FormEvent) => {
        
        //Makes it so that page doesn't refresh whenever you submit form
        e.preventDefault();
        if(!isLoaded) return;  

        //Core sign in call
        try{
            console.log("Attempting sign in...");
            const result = await signIn.create({
                identifier: email, password,
            });
            console.log("Sign in result:", result);
            
            //If sign in is successful 
            if(result.status == "complete"){
                await setActive({session: result.createdSessionId});
                router.push("/");
                console.log("Created session ID:", result.createdSessionId);
        

            }else{
                console.log("Sign in not complete:", result);
                setError("Sign in incomplete — check Clerk dashboard configuration.");
            }
        //Catching any errors 
        } catch (err: any){
            console.error("Sign in error:", err);
            setError(err.errors ? err.errors[0].message : "Sign in failed");
        }
    };

    //UI code section (jsx)

    return(
        <div className ="min-h-screen flex">
            <section className="w-full md:w-1/2 flex flex-col justify-center items-center bg-white p-8">
                <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
                    <h1 className='text-2X1 font-bold text-blue-600'>Sign in</h1>
                    <input 
                        className="border rounded-md p-2"
                        placeholder="Email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        />
                    <input  
                        className="border rounded-md p-2"
                        placeholder="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />                            
                    <button 
                        type="submit"
                        className="bg-orange-400 hover:bg-orange-600 text-white py-2 rounded-md"
                        >
                            Sign In
                        </button>
                </form>
            </section>

            <section className= "hidden md:block w-1/2 relative">
            <Image
                src="/GatorsWP.jpg"
                alt="SwampNotes background"
                fill
                className="object-cover w-full h-full"
                priority 
            />
            </section>
        </div>
    );
}