import React from "react"

import Head from "next/head"

import Example from "@components/table"

export default function Home({ games }) {
  return (
    <div>
      <Head>
        <title>0xCBB</title>

        <meta name="description" content="NCAABB Predictions" />

        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex justify-center min-h-screen py-10 bg-gradient-to-b from-gray-50 via-gray-50 to-gray-100">
        <div>
          <h1 className="px-5 text-2xl font-bold leading-tight tracking-tight text-center sm:mt-4 sm:text-6xl">
            Today's Games
          </h1>

          <h2 className="max-w-4xl px-10 mx-auto mt-8 text-base tracking-tight text-center text-gray-600 sm:text-2xl md:mt-5 md:text-2xl"></h2>

          <div className="px-4 sm:px-0">
            <Example people={games} />
            <p className="mt-6 text-xs font-medium text-center text-gray-600">
              Built by{" "}
              <a
                className="font-medium text-blue-600 transition duration-150 ease-in-out hover:text-blue-500 focus:outline-none focus:underline"
                href="https://twitter.com/0xAwill"
              >
                @0xAwill
              </a>
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

export async function getServerSideProps(ctx) {
  // get the current environment
  let dev = process.env.NODE_ENV !== "production"
  let { DEV_URL, PROD_URL } = process.env

  // request posts from api
  let response = await fetch(`${dev ? DEV_URL : PROD_URL}/api/daily`)
  // extract the data
  let data = await response.json()

  return {
    props: {
      games: data["message"],
    },
  }
}
