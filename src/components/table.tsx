export default function Example({ people }) {
  return (
    <div className="flex flex-col">
      <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div className="overflow-hidden border-b border-gray-200 shadow sm:rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                  >
                    Home
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                  >
                    Away
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                  >
                    Time
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                  >
                    Prediction
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {people.map((person) => (
                  <tr key={person.email}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {/*                        <div className="flex-shrink-0 w-10 h-10">
                          <img
                            className="w-10 h-10 rounded-full"
                            src={person.image}
                            alt=""
                          />
                        </div> */}
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {person.home}
                          </div>
                          {/*                           <div className="text-sm text-gray-500">
                            {person.email}
                          </div> */}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {person.away}
                      </div>
                      {/* <div className="text-sm text-gray-500">{person.away}</div> */}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex px-2 text-xs font-semibold text-green-800 bg-green-100 rounded-full leading-5">
                        Active
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                      {person.prediction}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
