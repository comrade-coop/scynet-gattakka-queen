/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ignite.scalar.examples

import org.apache.ignite.cluster.ClusterNode
import org.apache.ignite.scalar.scalar
import org.apache.ignite.scalar.scalar._

/**
 * Demonstrates various closure executions on the cloud using Scalar.
 * <p/>
 * Remote nodes should always be started with special configuration file which
 * enables P2P class loading: `'ignite.{sh|bat} examples/config/example-ignite.xml'`.
 * <p/>
 * Alternatively you can run `ExampleNodeStartup` in another JVM which will
 * start node with `examples/config/example-ignite.xml` configuration.
 */
object ScalarClosureExample {
  println("-" * 100)
  println("-" * 100)
  println("-" * 100)
  println("-" * 100)
    scalar("examples/config/example-ignite.xml") {
        println("><" * 25 + " process started " + "><" * 25)
        // topology()
        // helloWorld()
        helloWorld2()
        // broadcast()
        // greetRemotes()
        // greetRemotesAgain()
        println("*" * 50)
    }

    /**
     * Prints ignite topology.
     */
    def topology() {
        ignite$ foreach (n => println("Node: " + nid8$(n)))
    }

    /**
     * Obligatory example (2) - cloud enabled Hello World!
     */
    def helloWorld2() {
        // Notice the example usage of Java-side closure 'F.println(...)' and method 'scala'
        // that explicitly converts Java side object to a proper Scala counterpart.
        // This method is required since implicit conversion won't be applied here.
        var res = ignite$.run$(for (w <- "1w 2w 3w 4w 5w 6w 7w 8w 9w 10w 11w 12w 13w 14w 15w".split(" ")) yield () => {
            import scala.sys.process._
            import scala.io.Source
            import java.io.{IOException, File, PrintWriter}

            var stopping = true
            var errorText = ""
            var shouldPrintError = false

            var process: scala.sys.process.Process = null

            val io = new ProcessIO(
            in => {
                try {
                in.write(w.toArray.map(_.toByte))
                in.close()
                } catch {
                case _: IOException => println("Failed to write to input")
                }
                // in.close()
            },
            out => {
                val resultLines = scala.io.Source.fromInputStream(out).getLines.toList

                println(resultLines)
                out.close()

                // val resultMap = resultLines.view.map({line =>
                //     val parts = line.split("=", 2)
                //     if (parts.length == 2) Some((parts(0).trim, parts(1).trim))
                //     else None
                // }).flatten.toMap
                // out.close()

                // // println(f"Finished $shortHash")

                // if (resultMap.contains("score")) {

                //     val score = resultMap.getOrElse("score", "0").toDouble
                //     val displayScore = resultMap.getOrElse("display_score", "0").toDouble
                //     val iterations = resultMap.getOrElse("iterations", "-1").toInt
                //     println("-" * 50 + "> fitness is: " +  score)

                // } else if (!stopping) {
                //     // stop the process?
                // }
            },
            err => {
                // errorText = scala.io.Source.fromInputStream(err).mkString // The child usually dies if we don't wait for it to finish working
                // if (shouldPrintError) {
                //     printToFile(new File(f"../results/${shortHash}-error.txt")) { p =>
                //         p.println(s"chromosome = $strategy")
                //         p.println(errorText)
                //     }
                // }
                // println(errorText)
                err.close()
            })

            // println(w)
            process = Process(Seq("cmd.exe", "/c", "py", "D:\\coding\\test.py"), new File("../")) run io
            // println("cmd.exe /c dir".!!)
            // println(a)
        }, null)

        println("res   " + "-" * 20 + ">   ")
        println(res)
    }

    /**
     * Obligatory example - cloud enabled Hello World!
     */
    def helloWorld() {
        ignite$.run$("HELLO WORLD!".split(" ") map (w => () => println(w)), null)
    }

    /**
     * One way to execute closures on the ignite cluster.
     */
    def broadcast() {
        ignite$.bcastRun(() => println("Broadcasting!!!"), null)
    }

    /**
     *  Greats all remote nodes only.
     */
    def greetRemotes() {
        println("I AM HERE <" + "-" * 50)
        val me = ignite$.cluster().localNode.id

        // Note that usage Java-based closure.
        ignite$.cluster().forRemotes() match {
            case p if p.isEmpty => println("No remote nodes!")
            case p => p.bcastRun(() => println("Greetings from: " + me), null)
        }
    }

    /**
     * Same as previous greetings for all remote nodes but remote cluster group is filtered manually.
     */
    def greetRemotesAgain() {
        val me = ignite$.cluster().localNode.id

        // Just show that we can create any groups we like...
        // Note that usage of Java-based closure via 'F' typedef.
        ignite$.cluster().forPredicate((n: ClusterNode) => n.id != me) match {
            case p if p.isEmpty => println("No remote nodes!")
            case p => p.bcastRun(() => println("Greetings again from: " + me), null)
        }
    }
}
