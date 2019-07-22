package org.apache.ignite.scalar.examples

import java.util

import org.apache.ignite.compute.{ComputeJob, ComputeJobResult, ComputeTaskSplitAdapter}
import org.apache.ignite.scalar.scalar
import org.apache.ignite.scalar.scalar._

import scala.collection.JavaConversions._

object ScalarTaskExample extends App {
    var res: List[Double] = List()
    scalar("examples/config/example-ignite.xml") {
        res = ignite$.compute().execute(classOf[IgniteHelloWorld], "INSERT GENOME HERE")

    }
    
    // here we can use the result
    println("The result is " + res(0))



    class IgniteHelloWorld extends ComputeTaskSplitAdapter[String, List[Double]] {
        def split(clusterSize: Int, arg: String): java.util.Collection[_ <: ComputeJob] = {
            var w = arg
            Seq(toJob(() => {
                import scala.sys.process._
                import scala.io.Source
                import java.io.{IOException, File, PrintWriter}

                import scala.concurrent._
                import ExecutionContext.Implicits.global

                var lines:List[String] = List()

                var process: scala.sys.process.Process = null

                val io = new ProcessIO(
                in => {
                    try {
                    in.write(w.toArray.map(_.toByte))
                    in.close()
                    } catch {
                    case _: IOException => println("Failed to write to input")
                    }
                },
                out => {
                    // Get score for gattaka here??
                    val resultLines = scala.io.Source.fromInputStream(out).getLines.toList

                    lines = resultLines
                    out.close()
                },
                _.close())

                process = Process(Seq("cmd.exe", "/c", "py", "D:\\coding\\test.py"), new File("../")) run io
                val f = Future(blocking(process.exitValue()))
                val res = try {
                    Await.result(f, duration.Duration(10, "sec"))
                } catch {
                case _: TimeoutException => 
                    println("TIMEOUT!")
                    process.destroy()
                    process.exitValue()
                }
                lines
            }))
        }

        def reduce(results: util.List[ComputeJobResult]) = {
            // get result by result.getData
            // the result is all the lines from std out from the python
            var list: List[Double] = List()
            for (result <- results) {
                list ++= (result.getData())
            }

            list
        }
    }
}
